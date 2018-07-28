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

import time 
from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, osv
from datetime import datetime, date , timedelta
from openerp import exceptions
from openerp.exceptions import Warning



class ids_attendance_report(osv.osv_memory):
    _name = 'ids.attendance.report'
    _description = "IDS Attendance Report"
    _columns = {
                'emp_code'  : fields.char('Employee Code', size=5),
                'emp_name'  :fields.many2one('hr.employee', 'Employee Name'),
                'from_date' :fields.datetime('Date from'),
                'to_date'   :fields.datetime('Date to'),
                'department': fields.many2one('hr.department', 'Department'),
#                 'month'     : fields.selection([('jan', 'January'),('feb', 'February'),('mar', 'March'),('apr', 'April'),('may', 'May'),
#                                                  ('jun', 'June'),('jul', 'July'),('aug', 'August'),('sep', 'September'),
#                                                  ('oct', 'October'),('nov', 'November'),('dec', 'December')],'Month',),
                'output_type': fields.selection([('pdf', 'Portable Document (pdf)'),
                                                 ('xls', 'Excel Spreadsheet (xls)')],
                                                'Report format', help='Choose the format for the output', required=True),
                }
    
    _defaults = {
                'output_type'    : 'xls',
                }
    
    
    def print_attendance_report(self, cr, uid, ids, context=None):
        employee_obj = self.pool.get('hr.employee')
        employee_obj1 = self.pool.get('resource.resource')
        cr.execute("select id from hr_employee where id=(select id from resource_resource where user_id=%s)"%uid);
        empid = cr.fetchone()
        emp_level = employee_obj.search(cr, uid, [('parent_id', '=', empid)], context=context)
        if emp_level:
            if empid:
                emp_level.extend((empid))
        if not emp_level:
            uid = 1
            
        emp_second_level = employee_obj.search(cr, uid, [('parent_id', '=', emp_level)], context=context)
        emp_level.extend((emp_second_level))
        
        emp_third_level = employee_obj.search(cr, uid, [('parent_id', '=', emp_second_level)], context=context)
        emp_level.extend((emp_third_level))
 
        emp_fourth_level = employee_obj.search(cr, uid, [('parent_id', '=', emp_third_level)], context=context)
        emp_level.extend((emp_fourth_level))
        for case in self.browse(cr, uid, ids):
            data = {}
            data['ids'] = context.get('active_ids', [])
            data['model'] = context.get('active_model', 'ir.ui.menu')
            data['output_type'] =  case.output_type
            data['variables'] = {
                                'employee_code'  : case.emp_code or '',
                                'department': case.department.name or '',
                                'date_from' : case.from_date or '2016-01-01 00:00:00',
                                'date_to' : case.to_date or time.strftime('%Y-%m-%d %H:%M:%S'), 
                                'uid'         : uid and uid or 1,
                                'empid'       : empid or 0,
                                'emp_level'   : emp_level or 0,
                                'output_type' : case.output_type,
                                }
            print 'data', data
            return {
                    'type': 'ir.actions.report.xml',
                    'report_name':'ids_attendance_report',
                    'datas':data,
                    }