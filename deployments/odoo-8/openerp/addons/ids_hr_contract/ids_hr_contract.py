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

from __future__ import division
from openerp.osv import osv,fields
from lxml import etree
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

class hr_employee(osv.osv):
    _inherit='hr.employee'
                        
    def create(self, cr, uid, data, context=None):
        """Create record with the creation of new employee. """
        con_pool=self.pool.get('hr.contract')
        context = dict(context or {})
        if context.get("mail_broadcast"):
            context['mail_create_nolog'] = True
 
        employee_id = super(hr_employee, self).create(cr, uid, data, context=context)
        res={}
        name=data['name']
        job=data['job_id']
        employment_type=data['employment_type_id']
        res={
             'employee_id':employee_id,
             'name':"Salary Structure of"+" "+name,
             'job_id':job,
             'employment_type_id':employment_type,
             'type_id':1,
             'total':0,
             'total_pa':0,
             'deduction_total':0,
             'deduction_total_pa':0
             
             }
        contract_id=con_pool.create(cr,uid,res, context=context)
        if context.get("mail_broadcast"):
            self._broadcast_welcome(cr, uid, employee_id, context=context)
        return employee_id



class hr_contract(osv.osv):
    _inherit = 'hr.contract'
    _columns = {
                'active':fields.boolean('Active'),
                'confirmation_status':fields.selection([('yes','Yes'),('no','No'),('extended','Extended')],'Confirmation Status'),
                'date_start': fields.date('Start Date'),
                'wage': fields.float('Wage', digits=(16,2), help="Basic Salary of the employee"),
                'employment_type_id':fields.selection([('trainee','Trainee'),('regular','Regular'),('contract','Contractual'),('stipend','Stipend'),('consultant','Consultant')],'Employment Type', required=True),
                'tct'      : fields.float('Fixed P.M'),
                'tct_pm'   : fields.float('Total P.M'),
                'tct_pa'   : fields.float('Total Amount P.A'),
#                 'tct_amount'   : fields.float('TCT Amount', required=True),
                'basic'    : fields.float('Basic Salary'),
                'basic_pa' : fields.float('Basic Salary P.A'),
                'hra'      : fields.float('House Rent'),
                'hra_pa'   : fields.float('House Rent P.A'),
                'cca'      : fields.float('City Compensatory Allowance'),
                'cca_pa'   : fields.float('City Compensatory Allowance P.A'),
                'ta'       : fields.float('Transport Allowance'),
                'ta_pa'    : fields.float('Transport Allowance P.A'),
                'sa'       : fields.float('Special Allowance'),
                'sa_pa'    : fields.float('Special Allowance P.A'),
                'total'    : fields.float("Total", required=True),
                'total_pa' : fields.float("Total P.A", required=True),
                'pf_option': fields.selection([('yes','Yes'),('no','No')], 'PF Option'),
                'pf'       : fields.float('Provident Fund'),
                'pf_pa'    : fields.float('Provident Fund P.A'),
                'pf_deduction'  : fields.float('PF Deduction'),
                'pf_deduction_pa'  : fields.float('PF Deduction P.A'),
                'esi'      : fields.float('ESI'),
                'esi_pa'   : fields.float('ESI P.A'),
                'deduction_esi': fields.float('ESI'),
                'deduction_esi_pa': fields.float('ESI P.A'),
                'deduction_total': fields.float('Total Deduction', required=True),
                'deduction_total_pa': fields.float('Total Deduction P.A', required=True),
                'nps_option'   : fields.selection([('yes','Yes'),('no','No')], 'NPS Value'),
                'nps'      : fields.float('NPS'),
                'nps_pa'   : fields.float('NPS P.A'),
                'lb_option': fields.selection([('yes','Yes'),('no','No')], 'Loyalty Bonus Option'),
                'lb'       : fields.float('Loyalty Bonus'),
                'lb_pa'    : fields.float('Loyalty Bonus P.A'),
                'bonus'    : fields.float('Bonus'),
                'bonus_pa' : fields.float('Bonus P.A'),
                'ltc_option' : fields.selection([('yes','Yes'),('no','No')], 'LTC Option'),
                'ltc'      : fields.float('LTC'),
                'ltc_pa'   : fields.float('LTC P.A'),
                'meal_option'    : fields.selection([('yes','Yes'),('no','No')], 'Meal Voucher Option'),
                'meal'     : fields.float('Meal '),
                'meal_pa'  : fields.float('Meal P.A'),
                'conveyance_option': fields.selection([('yes','Yes'),('no','No')], 'Conveyance Option'),
                'conveyance'       : fields.float('Conveyance'),
                'conveyance_pa'    : fields.float('Conveyance P.A'),
                'magazine_option'  : fields.selection([('yes','Yes'),('no','No')], 'Bussiness Newspaper/Magazine Option'),
                'magazine' : fields.float('Bussiness Newspaper/Magazine'),
                'magazine_pa'      : fields.float('Bussiness Newspaper/Magazine P.A'),
                'landline_internet_option'    : fields.selection([('yes','Yes'),('no','No')], 'Landline/Broadband Option'),
                'landline_internet'    : fields.float('Landline/Broadband'),
                'landline_internet_pa' : fields.float('Landline/Broadband P.A'),
                'medical_option'       : fields.selection([('yes','Yes'),('no','No')], 'Medical Option'),
                'medical'   : fields.float('Medical'),
                'medical_pa': fields.float('Medical P.A'),
                'gratuity'  : fields.float('Gratuity'),
                'gratuity_pa'    : fields.float('Gratuity P.A'),
                'group_medical'  : fields.float('Group Medical Insurance'),
                'group_medical_pa'     : fields.float('Group Medical Insurance P.A'),
                'job_category'   : fields.selection([('staff','Staff'),('mgmt','Management')], 'Job Category'),
                'group_term'     : fields.float('Group Term Insurance'),
                'group_term_pa'  : fields.float('Group Term Insurance P.A'),
                'group_personal' : fields.float('Group Personal Accident Insurance'),
                'group_personal_pa'    : fields.float('Group Personal Accident Insurance P.A'),
                'fixed'     : fields.float('Fixed'),
                'fixed_pa'  : fields.float('Fixed P.A'),
                'fixed_benefit'  : fields.float('Fixed Benefit'),
                'fixed_benefit_pa'     : fields.float('Fixed Benefit P.A'),
                'age'       : fields.integer('Age'),
                'take_home' : fields.float('Net Take Home'),
                'take_home_pa'   : fields.float('Net Take Home P.A'),
                'variable_amount_pm': fields.float('Variable P.M'),
                'variable'  : fields.float('Variable'),
                'variable_pa'    : fields.float('Variable P.A'),
                'perf_variable'  : fields.float('Performance Variable'),
                'perf_variable_pa'  : fields.float('Performance Variable P.A'),
                'salary'       : fields.integer('Fixed + Benefit + Variable'),
                'salary_pa'       : fields.integer('Fixed + Benefit + Variable P.A'),
                'last_tctc': fields.float('Last TCTC'),
                'current_tctc': fields.float('Current TCTC'),
                'last_revision':fields.date('Last Revision'),
                'last_remark' : fields.char('Last Remark'),
                'mid_revision': fields.date('Mid Revision'),
                'mid_remark' : fields.char('Mid Remark'),
                'next_revision': fields.date('Next Revision'),
                'cycle' : fields.selection([('april','April'),('october','October'),('january','January'),('yearly','Yearly'),('other','Other')],'Cycle'),
                'anniversary_status': fields.selection([('na','NA'),('no','No'),('yes','Yes')],'Anniversary Status'),  
                
               
                
#                 contract salary structure
                'grade' : fields.selection([('aj1','AJ1'),('bj2','BJ2'),('cj3','CJ3')
                                            ,('de5','DE5'),('em5','EM5'),('em6','EM6'),('fm6','FM6')], 'Grade'),
                'dob' : fields.date('Date of Birth'),
                'gross' : fields.float('Gross'),
                'gross_pa' : fields.float('Gross P.A'),
                'empr_esi' : fields.float('Employer ESI'),
                'empr_esi_pa' : fields.float('Employer ESI P.A'),
                'emp_esi' : fields.float('Employee ESI'),
                'emp_esi_pa' : fields.float('Employee ESI P.A'),
                'in_hand' : fields.float('In hand'),
                'in_hand_pa' : fields.float('In hand P.A'),
                'ctc' : fields.float('CTC'),
                'ctc_pa' : fields.float('CTC P.A'),
                
                
               }
    
    _defaults = {
                 'pf_option': 'no',
                 'ltc_option': 'no',
                 'nps_option': 'no',
                'lb_option': 'no',
                'meal_option': 'no',
                'conveyance_option': 'no',
                'magazine_option': 'no',
                'landline_internet_option': 'no',
                'medical_option': 'no',
               # 'job_category' : 'staff',
                }
    
    
    def onchange_regular(self, cr, uid, ids, tct, chkwhich_bonus, chkwhich_esi, chkwhich_group_medical, chkwhich_group_term,
                     frmwhich_term, chkwhich_group_personal, tct_pm, pf_option, nps_option, lb_option, ltc_option, meal_option, conveyance_option,
                     magazine_option, landline_internet_option, medical_option, age, variable_amount_pm, employment_type_id,job_category, context=None):
        """Calculations are done with change of Basic Salary. """
        val = {}
        tct_pa = basic = basic_pa = hra = hra_pa = cca = cca_pa = ta = ta_pa = sa = sa_pa = 0
        pf = pf_pa = pf_deduction = pf_deduction_pa = nps = nps_pa = lb = lb_pa = ltc = ltc_pa = 0 
        meal = meal_pa = conveyance = conveyance_pa = magazine = magazine_pa = landline_internet = 0
        landline_internet_pa = medical = medical_pa = group_medical = group_medical_pa = group_term_pa = 0
        group_personal_pa = variable_amount = perf_variable = perf_variable_pa = total = total_pa = 0
        esi = esi_pa = deduction_esi = deduction_esi_pa = deduction_total = deduction_total = 0
        deduction_total_pa = fixed_benefit = fixed_benefit_pa = bonus = bonus_pa = gratuity = 0
        gratuity_pa = group_term = group_term_pa = group_personal = group_personal_pa = fixed = 0
        fixed_pa = take_home = take_home_pa = salary = salary_pa = 0
        print 'employment_type_id',employment_type_id 
        if tct or variable_amount_pm:
            tct_pm = tct + variable_amount_pm
            tct_pa = tct_pm * 12 
        basic = (tct_pm * 40)/100
        basic_pa = basic * 12
        hra = basic * 0.4
        hra_pa = hra * 12
        cca = basic * 0.15
        cca_pa = cca * 12
        ta = 1600
        ta_pa = ta * 12
        sa = tct_pm - (basic + hra + cca + ta)
        sa_pa = sa * 12
        total = basic + hra + cca + ta + sa
        print"total=====",total
        total_pa = total * 12
        if pf_option == 'yes':
            pf = basic * 0.12
            pf_pa = pf * 12
            pf_deduction = pf
            pf_deduction_pa = pf_pa
            sa = sa - pf
            sa_pa = sa * 12
#             total = total - pf
#             total_pa = total_pa -pf_pa
#         print 'chkwhich_esi',chkwhich_esi
        if total > 15000:
            esi = 0
        else:
            esi = round((total) * 0.0475)
            deduction_esi = round((total) * 0.0175)
#         if chkwhich_esi != esi:
             
        esi_pa = esi * 12
        deduction_esi_pa = deduction_esi * 12
        deduction_total = pf + deduction_esi
        deduction_total_pa = deduction_total * 12
         
        if nps_option == 'yes':
            nps = basic * 0.1
            nps_pa = nps * 12
            sa = sa - nps
            sa_pa = sa * 12
             
        if lb_option == 'yes':
            lb = 24000 / 12
            lb_pa = lb * 12
            sa = sa - lb
            sa_pa = sa * 12
             
        if (basic + cca) > 21000:
            bonus_pa = 0
            bonus = bonus * 12
        elif (basic + cca) > 7000:
            bonus_pa = 7000
            bonus = round(bonus_pa / 12)
            sa = sa - bonus
            sa_pa = sa * 12
#             total = total - bonus
#             total_pa = total_pa - bonus_pa
        else:
            bonus = round((basic + cca)/12)
            basic_cca = ((basic + cca) / float(12))
#             b_c = 6900 / float(12)
#             print 'zzzzzzzzz',b_c
#             print 'aaaaaaaaaaaaaaaaaaaaaaaa',basic_cca
            bonus_pa =  basic_cca * 12 
            sa = sa - bonus
            sa_pa = sa * 12
#             total = total - bonus
#             total_pa = total_pa - bonus_pa
#         print chkwhich_bonus
#         print 'bonus_after',bonus
#         print 'sa',sa
#         if chkwhich_bonus != bonus:
#             bonus_diff = chkwhich_bonus - bonus
#             print 'bonus_diff',bonus_diff
#             if chkwhich_bonus: 
#                 if chkwhich_bonus > bonus:
#                     sa = sa - bonus_diff
#                     bonus = chkwhich_bonus
#                     bonus_pa = bonus * 12
#                 if chkwhich_bonus < bonus:
#                     if bonus_diff < 0:
#                         bonus_diff = abs(bonus_diff)
#                     sa = sa + bonus_diff
#                     print 'bonus',bonus
                    
#                     bonus = chkwhich_bonus
         
        if ltc_option == 'yes':
            ltc = round((basic * 0.6) / 12)
            ltc_pa = ltc * 12
            sa = sa - ltc
            sa_pa = sa * 12
        if meal_option == 'yes':
            meal = 2200
            meal_pa = meal * 12
            sa = sa - meal
            sa_pa = sa * 12
        if conveyance_option == 'yes':
            conveyance = 1800
            conveyance_pa = conveyance * 12
            sa = sa - conveyance
            sa_pa = sa * 12
        if magazine_option == 'yes':
            magazine = 500
            magazine_pa = magazine * 12
            sa = sa - magazine
            sa_pa = sa * 12
        if landline_internet_option == 'yes':
            landline_internet = 750
            landline_internet_pa = landline_internet * 12
            sa = sa - landline_internet
            sa_pa = sa * 12
        if medical_option == 'yes':
            medical = 1250
            medical_pa = medical * 12
            sa = sa - medical
            sa_pa = sa * 12
        if employment_type_id == 'regular':
            gratuity = round((round((basic * 15)/26))/12) 
            gratuity_pa = (round((basic * 15)/26))
#         if not chkwhich_group_medical:
#         if chkwhich_group_medical != group_medical:
        if esi == 0:
            if employment_type_id == 'regular':
                if job_category == 'S':
                    if age <= 35:
                        group_medical_pa = 3900
                    elif age < 45:
                        group_medical_pa = 4260
                    elif age < 55:
                        group_medical_pa = 6180
                    elif age < 65:
                        group_medical_pa = 7080
                    else:
                        group_medical_pa = 0
                else:
                    if age <= 35:
                        group_medical_pa = 5050
                    elif age < 45:
                        group_medical_pa = 5500
                    elif age < 55:
                        group_medical_pa = 8100
                    elif age < 65:
                        group_medical_pa = 9300
                    else:
                        group_medical_pa = 0
        if employment_type_id == 'regular':
            group_medical = group_medical_pa / 12
        if chkwhich_group_medical != group_medical:
            if chkwhich_group_medical:
    #                 group_medical = chkwhich_group_medical
                group_medical_pa = chkwhich_group_medical * 12
        if employment_type_id == 'regular': 
            if job_category == 'staff':
                group_term_pa = 325
            else:
                group_term_pa = 535
            group_term = round(group_term_pa / 12)
        if employment_type_id == 'regular':
            if chkwhich_group_term != group_term:
                if chkwhich_group_term:
                    group_term = chkwhich_group_term
                    group_term_pa = group_term * 12 
        if esi == 0:
            group_personal_pa = 315
            group_personal = round(group_personal_pa / 12)
            if chkwhich_group_personal != group_personal:
                if chkwhich_group_personal:
                    group_personal = chkwhich_group_personal
                    group_personal_pa = group_personal * 12
        
        fixed = total + pf + esi + nps + lb + bonus + ltc + meal + conveyance + magazine + landline_internet + medical
        print"fixed=====",fixed
        fixed_pa = fixed * 12
        fixed_benefit = fixed + gratuity + group_medical + group_term + group_personal
        print"fixed_benefit",fixed_benefit
        fixed_benefit_pa = fixed_benefit * 12
        if variable_amount == 0:
            variable = 0
        if variable_amount_pm:
            perf_variable = variable_amount_pm
            perf_variable_pa = perf_variable * 12
        
        salary = fixed_benefit + perf_variable
        print"salary======",salary
        salary_pa = salary *12
#         print 'aaaaaaaaaaaaaaa',frmwhich_term
        
        total = basic + hra + cca + ta + sa
        total_pa = total * 12
        take_home = total - deduction_total
        take_home_pa = total_pa - deduction_total_pa
        val = {
#                'tct_amount' : tct_amount,
               'tct'    : tct,
               'tct_pm'    :tct_pm, 
               'tct_pa'    :tct_pa,
               'basic'     :basic,
               'basic_pa'  :basic_pa,
               'hra'       : hra,
               'hra_pa'    : hra_pa,
               'cca'   : cca,
               'cca_pa': cca_pa,
               'ta'    : ta,
               'ta_pa' : ta_pa,
               'sa'    : sa,
               'sa_pa' : sa_pa,
               'total' : total,
               'total_pa' : total_pa,
               'pf'    : pf,
               'pf_pa' : pf_pa,
               'pf_deduction'   : pf_deduction,
               'pf_deduction_pa': pf_deduction_pa,
               'esi'   : esi,
               'esi_pa': esi_pa,
               'deduction_esi'  : deduction_esi,
               'deduction_esi_pa'  : deduction_esi_pa,
               'deduction_total' : deduction_total,
               'deduction_total_pa' :   deduction_total_pa,
               'nps'   : nps,
               'nps_pa': nps_pa,
               'lb'    : lb,
               'lb_pa' : lb_pa,
               'bonus' : bonus,
               'bonus_pa'  : bonus_pa,
               'ltc'   : ltc,
               'ltc_pa': ltc_pa,
               'meal'  : meal,
               'meal_pa'   : meal_pa,
               'conveyance': conveyance,
               'conveyance_pa' : conveyance_pa,
               'magazine'  : magazine,
               'magazine_pa'   : magazine_pa,
               'landline_internet'    : landline_internet,
               'landline_internet_pa' : landline_internet_pa,
               'medical'   : medical,
               'medical_pa': medical_pa,
               'gratuity'  : gratuity,
               'gratuity_pa'   : gratuity_pa,
               'group_medical' : group_medical,
               'group_medical_pa' : group_medical_pa,
               'group_term' : group_term,
               'group_term_pa' : group_term_pa,
               'group_personal': group_personal,
               'group_personal_pa' : group_personal_pa,
               'fixed' : fixed,
               'fixed_pa' : fixed_pa,
               'fixed_benefit' : fixed_benefit,
               'fixed_benefit_pa' : fixed_benefit_pa,
               'take_home'  : take_home,
               'take_home_pa'   : take_home_pa,
               'perf_variable'  : perf_variable,
               'perf_variable_pa'  : perf_variable_pa,
               'salary' : salary,
               'salary_pa'  : salary_pa,
                }
        print 'regular salary structure', val
        return {'value':val}
    
    """ Edited by Satya """
    def onchange_meal(self, cr, uid, ids, sa,total,total_pa,meal,take_home,take_home_pa):
        """Meal Expenses Calculations. """
        spa=spa_pa=total1=total_pa1=meal_pa1=take_home1=take_home_pa1=0
        meal_pa1 = meal * 12
        spa = sa - meal
        spa_pa = spa*12
        total1 = total - meal
        total_pa1 = total1*12
        take_home1 = take_home-meal
        take_home_pa1 = take_home1*12
        val = {'meal_pa':meal_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
               }
        return {'value':val}
    def onchange_conveyance(self, cr, uid, ids, sa,total,total_pa,conveyance,take_home,take_home_pa):
        """ Conveyance Expenses Calculations."""
        spa=spa_pa=total1=total_pa1=conveyance_pa1=take_home1=take_home_pa1=0
        conveyance_pa1 = conveyance * 12
        spa = sa - conveyance
        spa_pa = spa*12
        total1 = total - conveyance
        total_pa1 = total1*12
        take_home1 = take_home-conveyance
        take_home_pa1 = take_home1*12
        val = {'conveyance_pa':conveyance_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
               }
        return {'value':val}
    def onchange_magazine(self, cr, uid, ids, sa,total,total_pa,magazine,take_home,take_home_pa):
        """Magazine Expenses Calculations. """
        spa=spa_pa=total1=total_pa1=magazine_pa1=0
        magazine_pa1 = magazine * 12
        spa = sa - magazine
        spa_pa = spa*12
        total1 = total - magazine
        total_pa1 = total1*12
        take_home1 = take_home-magazine
        take_home_pa1 = take_home1*12
        val = {'magazine_pa':magazine_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
               }
        return {'value':val}
    def onchange_landline_internet(self, cr, uid, ids, sa,total,total_pa,landline_internet,take_home,take_home_pa):
        """Landline Internet Expenses Calculations. """
        spa=spa_pa=total1=total_pa1=landline_internet_pa1=0
        landline_internet_pa1 = landline_internet * 12
        spa = sa - landline_internet
        spa_pa = spa*12
        total1 = total - landline_internet
        total_pa1 = total1*12
        take_home1 = take_home-landline_internet
        take_home_pa1 = take_home1*12
        val = {'landline_internet_pa':landline_internet_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
               }
        return {'value':val}
    def onchange_medical(self, cr, uid, ids, sa,total,total_pa,medical,take_home,take_home_pa):
        """Medical Insurance Calculations. """
        spa=spa_pa=total1=total_pa1=medical_pa1=0
        medical_pa1 = medical * 12
        spa = sa - medical
        spa_pa = spa*12
        total1 = total - medical
        total_pa1 = total1*12
        take_home1 = take_home-medical
        take_home_pa1 = take_home1*12
        val = {'medical_pa':medical_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
               }
        return {'value':val}
    
    
    
    def onchange_pf_option(self, cr, uid, ids, basic, sa,total,total_pa,pf,pf_pa,take_home,take_home_pa,salary,pf_option):
        """PF Calculations. """
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        pf1 =pf_pa1=pf_deduction=pf_deduction_pa=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if pf_option == 'yes':
            pf1 = basic * 0.12
            pf_pa1 = pf1 * 12
            pf_deduction = pf1
            pf_deduction_pa = pf_pa
            spa = sa - pf1
            spa_pa = spa*12
            total1 = total - pf1
            total_pa1 = total1*12
            take_home1 = take_home-pf_deduction
            take_home_pa1 = take_home1*12
#             salary1 = salary + pf1  
#             salary_pa1 = salary1 *12
        else:
            pf1=0.0
            pf_pa1=0.0
            pf_deduction = pf1
            pf_deduction_pa = pf_pa1
            spa = sa + pf
            spa_pa = spa*12
            total1 = total + pf
            total_pa1 = total1*12
            take_home1 = take_home+pf
            take_home_pa1 = take_home1*12
#             salary1 = salary - pf  
#             salary_pa1 = salary1 *12
        val = {'pf':pf1,
               'pf_pa':pf_pa1,
               'pf_deduction'   : pf_deduction,
               'pf_deduction_pa': pf_deduction_pa,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1
               }
        return {'value':val}
    def onchange_nps_option(self, cr, uid, ids, basic, sa,total,total_pa,nps,nps_pa,salary,nps_option,take_home,take_home_pa):
        """NPS Options Calculations. """
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        nps1 =nps_pa1=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if nps_option == 'yes':
            nps1 = basic * 0.1
            nps_pa1 = nps1 * 12
            spa = sa - nps1
            spa_pa = spa*12
            total1 = total - nps1
            total_pa1 = total1*12
            take_home1 = take_home-nps1
            take_home_pa1 = take_home1*12
#             salary1 = salary + nps1  
#             salary_pa1 = salary1 *12
        else:
            nps1=0.0
            nps_pa1=0.0
            spa = sa + nps
            spa_pa = spa*12
            total1 = total + nps
            total_pa1 = total1*12
            take_home1 = take_home+nps
            take_home_pa1 = take_home1*12
#             salary1 = salary - nps  
#             salary_pa1 = salary1 *12
        val = {'nps':nps1,
               'nps_pa':nps_pa1,
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
                'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1
               }
        return {'value':val}
    def onchange_ltc_option(self, cr, uid, ids, basic, sa,total,total_pa,ltc,ltc_pa,salary,ltc_option,take_home,take_home_pa):
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        ltc1 =ltc_pa1=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if ltc_option == 'yes':
            ltc1 = round((basic * 0.6) / 12)
            ltc_pa1 = ltc1 * 12
            spa = sa - ltc1
            spa_pa = spa*12
            total1 = total - ltc1
            total_pa1 = total1*12
            take_home1 = take_home-ltc1
            take_home_pa1 = take_home1*12
#             salary1 = salary + ltc1  
#             salary_pa1 = salary1 *12
        else:
            ltc1=0.0
            ltc_pa1=0.0
            spa = sa + ltc
            spa_pa = spa*12
            total1 = total + ltc
            total_pa1 = total1*12
            take_home1 = take_home+ltc
            take_home_pa1 = take_home1*12
#             salary1 = salary - ltc  
#             salary_pa1 = salary1 *12
        val = {'ltc':ltc1,
               'ltc_pa':ltc_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
                'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
               'total' : total1,
               'total_pa' : total_pa1
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
               }
        return {'value':val}
    def onchange_lb_option(self, cr, uid, ids, basic, sa,total,total_pa,lb,lb_pa,salary,lb_option,take_home,take_home_pa):
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        lb1 =lb_pa1=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if lb_option == 'yes':
            lb1 = 24000 / 12
            lb_pa1 = lb1 * 12
            spa = sa - lb1
            spa_pa = spa*12
            total1 = total - lb1
            total_pa1 = total1*12
            take_home1 = take_home-lb1
            take_home_pa1 = take_home1*12
#             salary1 = salary + lb1 
#             salary_pa1 = salary1 *12
        else:
            lb1=0.0
            lb_pa1=0.0
            spa = sa + lb
            spa_pa = spa*12
            total1 = total + lb
            total_pa1 = total1*12
            take_home1 = take_home+lb
            take_home_pa1 = take_home1*12
#             salary1 = salary - lb  
#             salary_pa1 = salary1 *12
        val = {'lb':lb1,
               'lb_pa':lb_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
               'total' : total1,
               'total_pa' : total_pa1
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
               }
        return {'value':val}
    
    
    def onchange_meal_option(self, cr, uid, ids, basic, sa,total,total_pa,meal,meal_pa,salary,meal_option,take_home,take_home_pa):
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        meal1 =meal_pa1=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if meal_option == 'yes':
            meal1 = 0
            meal_pa1 = meal1 * 12
            spa = sa - meal1
            spa_pa = spa*12
            total1 = total - meal1
            total_pa1 = total1*12
            take_home1 = take_home-meal1
            take_home_pa1 = take_home1*12
#             salary1 = salary + meal1 
#             salary_pa1 = salary1 *12
        else:
            meal1=0.0
            meal_pa1=0.0
            spa = sa + meal
            spa_pa = spa*12
            total1 = total + meal
            total_pa1 = total1*12
            take_home1 = take_home+meal
            take_home_pa1 = take_home1*12
#             salary1 = salary - meal  
#             salary_pa1 = salary1 *12
        val = {'meal':meal1,
               'meal_pa':meal_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
               }
        return {'value':val}
    
    
    def onchange_conveyance_option(self, cr, uid, ids, basic, sa,total,total_pa,conveyance,conveyance_pa,salary,conveyance_option,take_home,take_home_pa):
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        conveyance1=conveyance_pa1=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if conveyance_option == 'yes':
            conveyance1 = 0
            conveyance_pa1 = conveyance1 * 12
            spa = sa - conveyance1
            spa_pa = spa*12
            total1 = total - conveyance1
            total_pa1 = total1*12
            take_home1 = take_home-conveyance1
            take_home_pa1 = take_home1*12
#             salary1 = salary + conveyance1 
#             salary_pa1 = salary1 *12
        else:
            conveyance1=0.0
            conveyance_pa1=0.0
            spa = sa + conveyance
            spa_pa = spa*12
            total1 = total + conveyance
            total_pa1 = total1*12
            take_home1 = take_home+conveyance
            take_home_pa1 = take_home1*12
#             salary1 = salary - conveyance  
#             salary_pa1 = salary1 *12
        val = {'conveyance':conveyance1,
               'conveyance_pa':conveyance_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
               }
        return {'value':val}
    
    def onchange_magazine_option(self, cr, uid, ids, basic, sa,total,total_pa,magazine,magazine_pa,salary,magazine_option,take_home,take_home_pa):
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        magazine1=magazine_pa1=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if magazine_option == 'yes':
            magazine1 = 0
            magazine_pa1 = magazine1 * 12
            spa = sa - magazine1
            spa_pa = spa*12
            total1 = total - magazine1
            total_pa1 = total1*12
            take_home1 = take_home-magazine1
            take_home_pa1 = take_home1*12
#             salary1 = salary + magazine1 
#             salary_pa1 = salary1 *12
        else:
            magazine1=0.0
            magazine_pa1=0.0
            spa = sa + magazine
            spa_pa = spa*12
            total1 = total + magazine
            total_pa1 = total1*12
            take_home1 = take_home+magazine
            take_home_pa1 = take_home1*12
#             salary1 = salary - magazine  
#             salary_pa1 = salary1 *12
        val = {'magazine':magazine1,
               'magazine_pa':magazine_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
               }
        return {'value':val}
    
    def onchange_landline_option(self, cr, uid, ids, basic, sa,total,total_pa,landline_internet,landline_internet_pa,salary,landline_internet_option,take_home,take_home_pa):
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        landline_internet1=landline_internet_pa1=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if landline_internet_option == 'yes':
            landline_internet1 = 0
            landline_internet_pa1 = landline_internet1 * 12
            spa = sa - landline_internet1
            spa_pa = spa*12
            total1 = total - landline_internet1
            total_pa1 = total1*12
            take_home1 = take_home-landline_internet1
            take_home_pa1 = take_home1*12
#             salary1 = salary + landline_internet1 
#             salary_pa1 = salary1 *12
        else:
            landline_internet1=0.0
            landline_internet_pa1=0.0
            spa = sa + landline_internet
            spa_pa = spa*12
            total1 = total + landline_internet
            total_pa1 = total1*12
            take_home1 = take_home+landline_internet
            take_home_pa1 = take_home1*12
#             salary1 = salary - landline_internet  
#             salary_pa1 = salary1 *12
        val = {'landline_internet':landline_internet1,
               'landline_internet_pa':landline_internet_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
               }
        return {'value':val}
    
    def onchange_medical_option(self, cr, uid, ids, basic, sa,total,total_pa,medical,medical_pa,salary,medical_option,take_home,take_home_pa):
        print"basic,sa,total,total_pa",basic,sa,total,total_pa
        medical1=medical_pa1=spa=spa_pa=total1=total_pa1=take_home1=take_home_pa1=0
        if medical_option == 'yes':
            medical1 = 0
            medical_pa1 = medical1 * 12
            spa = sa - medical1
            spa_pa = spa*12
            total1 = total - medical1
            total_pa1 = total1*12
            take_home1 = take_home-medical1
            take_home_pa1 = take_home1*12
#             salary1 = salary + medical1 
#             salary_pa1 = salary1 *12
        else:
            medical1=0.0
            medical_pa1=0.0
            spa = sa + medical
            spa_pa = spa*12
            total1 = total + medical
            total_pa1 = total1*12
            take_home1 = take_home+medical
            take_home_pa1 = take_home1*12
#             salary1 = salary - medical  
#             salary_pa1 = salary1 *12
        val = {'medical':medical1,
               'medical_pa':medical_pa1,
               'sa' : spa,
               'sa_pa' : spa_pa,
               'total' : total1,
               'total_pa' : total_pa1,
               'take_home' : take_home1,
               'take_home_pa': take_home_pa1,
#                'salary' : salary1,
#                'salary_pa' : salary_pa1,
               }
        return {'value':val}
    
    
    
        
        
    def onchange_basic(self, cr, uid, ids, basic,cca,sa,hra,ta,tct,group_medical,group_term,group_personal,perf_variable,employment_type_id):
        """Basic Salary Calculations. """
        bonus=bonus_pa=spa=spa_pa=basic_cca=gratuity=gratuity_pa=0
        house_rent=basic*.4
        conveyance = basic * 0.15
        
        if (basic + cca) > 21000:
            bonus_pa = 0
            bonus = 0
            spa = tct-(basic+house_rent+conveyance+ta+bonus)
            spa_pa = spa * 12
        elif (basic + cca) > 7000:
            bonus_pa = 7000
            bonus = round(bonus_pa / 12)
            spa = tct-(basic+house_rent+conveyance+ta+bonus)
            spa_pa = spa * 12
        else:
            bonus = round((basic + cca)/12)
            basic_cca = ((basic + cca) / float(12))
            bonus_pa =  basic_cca * 12 
            spa = tct-(basic+house_rent+conveyance+ta+bonus)
            spa_pa = spa * 12
        
        if employment_type_id == 'regular':
            gratuity = round((round((basic * 15)/26))/12) 
            gratuity_pa = (round((basic * 15)/26))
        basic_pa = basic*12 
        total= basic+house_rent+conveyance+ta+spa
        fixed = total + bonus
        salary = fixed + gratuity + group_medical + group_term + group_personal + perf_variable  
        salary_pa = salary *12
       
        val = {'basic_pa':basic_pa,
               'gratuity':gratuity,
               'gratuity_pa':gratuity_pa,
               'sa'    : spa,
               'sa_pa' : spa_pa,
               'bonus' : bonus,
               'bonus_pa'  : bonus_pa,
               'total' : total,
               'hra' : house_rent,
               'cca' : conveyance,
               'take_home': total,
               'salary' : salary,
               'salary_pa'  : salary_pa,
               }
        return {'value':val}
    
    def onchange_hra(self, cr, uid, ids, basic,hra,cca,ta,sa,tct,bonus,gratuity,group_medical,group_term,group_personal,perf_variable):
        hra_pa = hra*12
        spa = tct-(basic+hra+cca+ta+bonus)
        spa_pa = spa * 12
        total= basic+hra+cca+ta+spa
        fixed = total + bonus
        salary = fixed + gratuity + group_medical + group_term + group_personal + perf_variable  
        salary_pa = salary *12
        val = {'hra_pa':hra_pa,
               'sa'    : spa,
               'sa_pa' : spa_pa,
               'total' : total,
               'salary' : salary,
               'salary_pa'  : salary_pa,
               }
        return {'value':val}
    
    def onchange_cca(self, cr, uid, ids, cca, basic, sa, hra, ta, tct,gratuity,group_medical,group_term,group_personal,perf_variable):
        bonus=bonus_pa=spa=spa_pa=basic_cca=0
        if (basic + cca) > 21000:
            bonus_pa = 0
            bonus = 0
            spa = tct-(basic+hra+cca+ta+bonus)
            spa_pa = spa * 12
        elif (basic + cca) > 7000:
            bonus_pa = 7000
            bonus = round(bonus_pa / 12)
            spa = tct-(basic+hra+cca+ta+bonus)
            spa_pa = spa * 12
        else:
            bonus = round((basic + cca)/12)
            basic_cca = ((basic + cca) / float(12))
            bonus_pa =  basic_cca * 12 
            spa = tct-(basic+hra+cca+ta+bonus)
            spa_pa = spa * 12
        cca_pa = cca*12
        total= basic+hra+cca+ta+spa
        fixed = total + bonus
        salary = fixed + gratuity + group_medical + group_term + group_personal + perf_variable  
        salary_pa = salary *12
        val = {'cca_pa':cca_pa,
               'sa'    : spa,
               'sa_pa' : spa_pa,
               'bonus' : bonus,
               'bonus_pa'  : bonus_pa,
               'total' : total,
               'take_home': total,
               'salary' : salary,
               'salary_pa'  : salary_pa,
               }
        return {'value':val}
    
    def onchange_ta(self, cr, uid, ids, ta):
        ta_pa = ta*12
        val = {'ta_pa':ta_pa}
        return {'value':val}
    
    def onchange_sa(self, cr, uid, ids, basic,hra,cca,ta,sa,tct,bonus,gratuity,group_medical,group_term,group_personal,perf_variable):
        sa_pa = sa*12
        total= basic+hra+cca+ta+sa
#         fixed = total + bonus
#         salary = fixed + gratuity + group_medical + group_term + group_personal + perf_variable  
#         salary_pa = salary *12
        val = {'sa_pa':sa_pa,
               'total' : total,
#                'salary' : salary,
#                'salary_pa'  : salary_pa,
               }
        return {'value':val}
    
    def onchange_pfoption(self, cr, uid, ids, pf_option, basic):
        val = {}
        if pf_option == 'yes':
            pf = basic*0.12
            val = {'pf':pf}
        return {'value':val}
    
    def onchange_esi(self, cr, uid, ids, esi):
        val = {}
        if not esi:
            val = {'group_personal_pa' : 315,
                   'group_personal' : round(315/12)} 
        return {'value':val}
    
    def onchange_bonus(self, cr, uid, ids, bonus, chkwch, sa, sa_pa):
        val = {}
        print 'asdfasdfsadfasdf',bonus
        print 'onchange_chkwch',chkwch
        if bonus:
            sa = sa - bonus
            bonus_pa = bonus * 12
#         bonus = sa*12
        val = {'bonus':bonus,
               'sa': sa,
               'bonus_pa':bonus_pa}
        return {'value':val}
    
    
    
    def onchange_trainee(self, cr, uid, ids, gross, empr_esi, emp_esi, in_hand, ctc):
        empr_esi = emp_esi = in_hand = ctc = 0
        val = {}
        gross_pa = gross * 12
        empr_esi = round(gross * 0.0475)
        empr_esi_pa = empr_esi * 12
        emp_esi = round(gross * 0.0175)
        emp_esi_pa = emp_esi * 12
        in_hand = gross - emp_esi
        in_hand_pa = in_hand * 12
        ctc = gross + empr_esi
        ctc_pa = ctc * 12
        val = {'gross' : gross,
               'gross_pa' : gross_pa,
               'empr_esi' : empr_esi,
               'empr_esi_pa' : empr_esi_pa,
               'emp_esi' : emp_esi,
               'emp_esi_pa' : emp_esi_pa,
               'in_hand' : in_hand,
               'in_hand_pa' : in_hand_pa,
               'ctc' : ctc,
               'ctc_pa' : ctc_pa,
               }
        print 'trainee salary structure', val
        return {'value':val}




    
    
    
    def onchange_contract(self, cr, uid, ids, tct, chkwhich_bonus, chkwhich_esi, chkwhich_group_medical, chkwhich_group_term,
                     frmwhich_term, chkwhich_group_personal, tct_pm, pf_option, nps_option, lb_option, ltc_option, meal_option, conveyance_option,
                     magazine_option, landline_internet_option, medical_option, age, variable_amount_pm, context=None):
        val = {}
        tct_pa = basic = basic_pa = hra = hra_pa = cca = cca_pa = ta = ta_pa = sa = sa_pa = 0
        pf = pf_pa = pf_deduction = pf_deduction_pa = nps = nps_pa = lb = lb_pa = ltc = ltc_pa = 0 
        meal = meal_pa = conveyance = conveyance_pa = magazine = magazine_pa = landline_internet = 0
        landline_internet_pa = medical = medical_pa = group_medical = group_medical_pa = group_term_pa = 0
        group_personal_pa = variable_amount = perf_variable = perf_variable_pa = total = total_pa = 0
        esi = esi_pa = deduction_esi = deduction_esi_pa = deduction_total = deduction_total = 0
        deduction_total_pa = fixed_benefit = fixed_benefit_pa = bonus = bonus_pa = gratuity = 0
        gratuity_pa = group_term = group_term_pa = group_personal = group_personal_pa = fixed = 0
        fixed_pa = take_home = take_home_pa = salary = salary_pa = 0
        if tct or variable_amount_pm:
            tct_pm = tct + variable_amount_pm
            tct_pa = tct_pm * 12 
        basic = (tct_pm * 40)/100
        basic_pa = basic * 12
        hra = basic * 0.4
        hra_pa = hra * 12
        cca = basic * 0.15
        cca_pa = cca * 12
        ta = 1600
        ta_pa = ta * 12
        sa = tct_pm - (basic + hra + cca + ta)
        sa_pa = sa * 12
        total = basic + hra + cca + ta + sa - sa
        total_pa = total * 12
        if pf_option == 'yes':
            pf = basic * 0.12
            pf_pa = pf * 12
            pf_deduction = pf
            pf_deduction_pa = pf_pa
            sa = sa - pf
            sa_pa = sa * 12
        if total > 15000:
            esi = 0
        else:
            esi = round((total) * 0.0475)
            deduction_esi = round((total) * 0.0175)
        esi_pa = esi * 12
        deduction_esi_pa = deduction_esi * 12
        deduction_total = pf + deduction_esi
        deduction_total_pa = deduction_total * 12
         
        if nps_option == 'yes':
            nps = basic * 0.1
            nps_pa = nps * 12
            sa = sa - nps
            sa_pa = sa * 12
        if lb_option == 'yes':
            lb = 24000 / 12
            lb_pa = lb * 12
            sa = sa - lb
            sa_pa = sa * 12
        if (basic + cca) > 21000:
            bonus_pa = 0
            bonus = bonus * 12
        elif (basic + cca) > 7000:
            bonus_pa = 7000
            bonus = round(bonus_pa / 12)
            sa = sa - bonus
            sa_pa = sa * 12
        else:
            bonus = round((basic + cca)/12)
            basic_cca = ((basic + cca) / float(12))
            bonus_pa =  basic_cca * 12 
            sa = sa - bonus
            sa_pa = sa * 12
        if ltc_option == 'yes':
            ltc = round((basic * 0.6) / 12)
            ltc_pa = ltc * 12
            sa = sa - ltc
            sa_pa = sa * 12
        if meal_option == 'yes':
            meal = 2200
            meal_pa = meal * 12
            sa = sa - meal
            sa_pa = sa * 12
        if conveyance_option == 'yes':
            conveyance = 1800
            conveyance_pa = conveyance * 12
            sa = sa - conveyance
            sa_pa = sa * 12
        if magazine_option == 'yes':
            magazine = 500
            magazine_pa = magazine * 12
            sa = sa - magazine
            sa_pa = sa * 12
        if landline_internet_option == 'yes':
            landline_internet = 750
            landline_internet_pa = landline_internet * 12
            sa = sa - landline_internet
            sa_pa = sa * 12
        if medical_option == 'yes':
            medical = 1250
            medical_pa = medical * 12
            sa = sa - medical
            sa_pa = sa * 12
        gratuity = 0
        gratuity_pa = 0
#         if esi == 0:
#             if job_category == 'staff':
#                 if age <= 35:
#                     group_medical_pa = 3900
#                 elif age < 45:
#                     group_medical_pa = 4260
#                 elif age < 55:
#                     group_medical_pa = 6180
#                 elif age < 65:
#                     group_medical_pa = 7080
#                 else:
#                     group_medical_pa = 0
#             else:
#                 if age <= 35:
#                     group_medical_pa = 5050
#                 elif age < 45:
#                     group_medical_pa = 5500
#                 elif age < 55:
#                     group_medical_pa = 8100
#                 elif age < 65:
#                     group_medical_pa = 9300
#                 else:
#                     group_medical_pa = 0
#             group_medical = 0
        if chkwhich_group_medical != group_medical:
            print 'chkwhich_group_medical',chkwhich_group_medical,
            if chkwhich_group_medical:
                group_medical_pa = chkwhich_group_medical * 12
#         if job_category == 'staff':
#             group_term_pa = 0
#         else:
#             group_term_pa = 0
        group_term = 0
        if esi == 0:
            group_personal_pa = 315
            group_personal = round(group_personal_pa / 12)
            if chkwhich_group_personal != group_personal:
                if chkwhich_group_personal:
                    group_personal = chkwhich_group_personal
                    group_personal_pa = group_personal * 12
        
        fixed = total + pf + esi + nps + lb + bonus + ltc + meal + conveyance + magazine + landline_internet + medical
        fixed_pa = fixed * 12
        fixed_benefit = fixed + gratuity + group_medical + group_term + group_personal
        fixed_benefit_pa = fixed_benefit * 12
        if variable_amount == 0:
            variable = 0
        if variable_amount_pm:
            perf_variable = variable_amount_pm
            perf_variable_pa = perf_variable * 12
        
        salary = fixed_benefit + perf_variable
        salary_pa = salary *12
        total = basic + hra + cca + ta + sa
        total_pa = total * 12
        take_home = total - deduction_total
        take_home_pa = total_pa - deduction_total_pa
        val = {
               'tct'    : tct,
               'tct_pm'    :tct_pm, 
               'tct_pa'    :tct_pa,
               'basic'     :basic,
               'basic_pa'  :basic_pa,
               'hra'       : hra,
               'hra_pa'    : hra_pa,
               'cca'   : cca,
               'cca_pa': cca_pa,
               'ta'    : ta,
               'ta_pa' : ta_pa,
               'sa'    : sa,
               'sa_pa' : sa_pa,
               'total' : total,
               'total_pa' : total_pa,
               'pf'    : pf,
               'pf_pa' : pf_pa,
               'pf_deduction'   : pf_deduction,
               'pf_deduction_pa': pf_deduction_pa,
               'esi'   : esi,
               'esi_pa': esi_pa,
               'deduction_esi'  : deduction_esi,
               'deduction_esi_pa'  : deduction_esi_pa,
               'deduction_total' : deduction_total,
               'deduction_total_pa' :   deduction_total_pa,
               'nps'   : nps,
               'nps_pa': nps_pa,
               'lb'    : lb,
               'lb_pa' : lb_pa,
               'bonus' : bonus,
               'bonus_pa'  : bonus_pa,
               'ltc'   : ltc,
               'ltc_pa': ltc_pa,
               'meal'  : meal,
               'meal_pa'   : meal_pa,
               'conveyance': conveyance,
               'conveyance_pa' : conveyance_pa,
               'magazine'  : magazine,
               'magazine_pa'   : magazine_pa,
               'landline_internet'    : landline_internet,
               'landline_internet_pa' : landline_internet_pa,
               'medical'   : medical,
               'medical_pa': medical_pa,
               'gratuity'  : gratuity,
               'gratuity_pa'   : gratuity_pa,
               'group_medical' : group_medical,
               'group_medical_pa' : group_medical_pa,
               'group_term' : group_term,
               'group_term_pa' : group_term_pa,
               'group_personal': group_personal,
               'group_personal_pa' : group_personal_pa,
               'fixed' : fixed,
               'fixed_pa' : fixed_pa,
               'fixed_benefit' : fixed_benefit,
               'fixed_benefit_pa' : fixed_benefit_pa,
               'take_home'  : take_home,
               'take_home_pa'   : take_home_pa,
               'perf_variable'  : perf_variable,
               'perf_variable_pa'  : perf_variable_pa,
               'salary' : salary,
               'salary_pa'  : salary_pa,
                }
        print 'contract salary structure', val
        return {'value':val}
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    