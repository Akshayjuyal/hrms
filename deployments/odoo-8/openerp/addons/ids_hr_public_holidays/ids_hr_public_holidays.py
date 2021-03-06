# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv, fields
import time
from openerp import netsvc
from datetime import date
from openerp.tools.translate import _

class ids_hr_public_holidays(osv.osv):
    
    _name = 'ids.hr.public.holidays'
    _description = 'Public Holidays'
    YEAR_LIST = [(num, str(num)) for num in range((time.localtime().tm_year+1), (time.localtime().tm_year-2), -1)]
    _columns = {
                'year': fields.selection(YEAR_LIST,"Calendar Year", required=True),
                'active':fields.boolean('Active'),
                'company_id':fields.many2one('res.company', 'Company'),
                'division_id':fields.many2one('division','Division'),
                'location_id': fields.many2one('office.location', 'Location'),
                'department_id':fields.many2one('hr.department','Department'),
                'department_ids':fields.many2many('hr.department', 'department_rel', 'holiday_id','department','Department'),
                'line_ids': fields.one2many('ids.hr.public.holidays.line', 'holidays_id', 'Holiday Dates')
    }
    
    _rec_name = 'year'
    _order = "year"
    
#     _sql_constraints = [
#         ('year_unique', 'UNIQUE(year)', _('Duplicate year!')),
#     ]
    
    def create(self, cr, uid, values, context=None):
        
        data_search=self.search(cr,uid,[('year','=',values['year']),('department_id','=',values['department_id']),('division_id','=',values['division_id']),('location_id','=',values['location_id'])])
        if data_search:
            raise osv.except_osv(_('Warning'), _('Public holidays record already exists! Please update the existing record.'))
        id = super(ids_hr_public_holidays, self).create(cr, uid, values, context)
        return id
    
    def is_public_holiday(self, cr, uid, dt, context=None):

        ph_obj = self.pool.get('ids.hr.public.holidays')
        ph_ids = ph_obj.search(cr, uid, [
                                         ('year', '=', dt.year),
                                        ],
                               context=context)
        if len(ph_ids) == 0: return False
        
        for line in ph_obj.browse(cr, uid, ph_ids[0], context=context).line_ids:
            if date.strftime(dt, "%Y-%m-%d") == line.date:
                return True
        
        return False
    
    def get_holidays_list(self, cr, uid, year, context=None):

        res = []
        ph_ids = self.search(cr, uid, [('year', '=', year)], context=context)
        if len(ph_ids) == 0:
            return res
        [res.append(l.date) for l in self.browse(cr, uid, ph_ids[0], context=context).line_ids]
        return res
    
    def allocate_public_holiday(self, cr, uid, ids, context=None):
        """Allocating public holidays. """
        obj_res_public_holiday_line = self.pool.get('ids.hr.public.holidays.line')
        obj_res_employee = self.pool.get('hr.employee')
        obj_res_holiday = self.pool.get('hr.holidays')
        obj_res_holiday_status_obj = self.pool.get('hr.holidays.status').search(cr, uid, [('code','=', 'NHD')])
        if len(obj_res_holiday_status_obj):
            HOLIDAY_STATUS_ID = obj_res_holiday_status_obj[0]        
        else:
            HOLIDAY_STATUS_ID = 0
        
        if HOLIDAY_STATUS_ID:
            for i in range(0,2):
                if i == 0:
                    #Code will run when new public holiday is added and allocated
                    obj_res_public_holiday_line_ids = obj_res_public_holiday_line.search(cr, uid, [('holidays_id','in', ids),('allocated','=',False)])
                    obj_res_employee_ids = obj_res_employee.search(cr, uid, [('emp_code','!=', False),('active','=', 1),('public_holiday_allocated','=', True)])
                elif i==1:
                    #Code will run when new employee is added
                    obj_res_public_holiday_line_ids = obj_res_public_holiday_line.search(cr, uid, [('holidays_id','in', ids)])
                    obj_res_employee_ids = obj_res_employee.search(cr, uid, [('emp_code','!=', False),('active','=', 1),('public_holiday_allocated','=', False)])
                   
                allocated_holiday_ids = []
                requested_holiday_ids = []
                
                #Allocate & Approve public holidays to all active employees
                for employee_id in obj_res_employee_ids:
                    vals = {
                        'holiday_status_id': HOLIDAY_STATUS_ID,
                        'employee_id':employee_id,
                        'name': 'Public Holiday',
                        'number_of_days_temp': float(len(obj_res_public_holiday_line_ids)),
                        'number_of_days': len(obj_res_public_holiday_line_ids),
                        'holiday_type': 'employee',
                        'state': 'confirm',
                        'manager_id':1,
                        'type': 'add'
                    }
                    allocated_holiday_ids.append(obj_res_holiday.create(cr, uid, vals, context=context))
                
                for allocated_holiday_id in allocated_holiday_ids:
                    obj_res_holiday.write(cr, uid, [allocated_holiday_id], {'state':'validate'})
                    
                    
                #Create & Approve automatic public holiday requests to all active employees
                for public_holiday_id in obj_res_public_holiday_line_ids:
                    public_holiday_detail = obj_res_public_holiday_line.browse(cr, uid, public_holiday_id)
                    for employee_id in obj_res_employee_ids:
                        vals = {
                            'holiday_status_id': HOLIDAY_STATUS_ID,
                            'date_to': public_holiday_detail.date+' 18:00:00',
                            'employee_id':employee_id,
                            'name': public_holiday_detail.name,
                            'number_of_days_temp': 1,
                            'date_from': public_holiday_detail.date+' 10:00:00',
                            'number_of_days': -1,
                            'holiday_type': 'employee',
                            'state': 'confirm',
                            'manager_id':1,
                            'type': 'remove'
                        }
                        requested_holiday_ids.append(obj_res_holiday.create(cr, uid, vals, context=context))
                        obj_res_public_holiday_line.write(cr, uid, [public_holiday_id], {'allocated':True})
                        
                        if i==1:
                            obj_res_employee.write(cr, uid, [employee_id], {'public_holiday_allocated':True})
                            
                #Validate request & create corresponding entries in hr.holidays, resource_calendar_leaves, crm_meeting tables
                obj_res_holiday.holidays_validate(cr,uid,requested_holiday_ids)
            
        return True
            
class ids_hr_public_holidays_line(osv.osv):
    
    _name = 'ids.hr.public.holidays.line'
    _description = 'Public Holidays Line'    
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'date': fields.date('Date', required=True),
        'allocated': fields.boolean('Allocated'),
        'holidays_id': fields.many2one('ids.hr.public.holidays', 'Holiday Calendar Year')                
    }
    
    _defaults = {
        'allocated': False,   
    }
    
    _order = "date, name desc"
    
class hr_employee(osv.osv):
    
    _inherit="hr.employee"
    _name = 'hr.employee'
    
    _columns = {      
        'public_holiday_allocated': fields.boolean('Allocated')                   
    }
    
    _defaults = {
        'public_holiday_allocated': False,   
    }
    
    def _check_unique_insesitive(self, cr, uid, ids, context=None):
        """Check uniqueness of record. """
        list_ids = self.search(cr, uid , [], context=context)
        lst = [list_id.name.lower() for list_id in self.browse(cr, uid, list_ids, context=context) if list_id.name and list_id.id not in ids]
        for self_obj in self.browse(cr, uid, ids, context=context):
            if self_obj.name and self_obj.name.lower() in lst:
                return False
            return True

class hr_holidays_status(osv.osv):
    
    _inherit="hr.holidays.status"
    _name = "hr.holidays.status"
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', _('Duplicate Leave Type!')),
    ]
   # _constraints = [(_check_unique_insesitive, 'Duplicate Leave Type!', ['name'])]
    
