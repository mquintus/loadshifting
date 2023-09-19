from unittest import TestCase
import sys
import pandas as pd
import pytest

sys.path.append('../../../cpuc-dynamic-pricing/')
sys.path.append('../../../cpuc-dynamic-pricing/cpuc_dynamic_pricing/')
sys.path.append('../')
#from Dot_Progress_Bar import Dot_Progress_Bar
from Tech_Models.basicshifter import Basic_Shifter

class TryTesting(TestCase):
    def test_not_logged_in(self):
        assert True
        pass
      
    def test_simple_shift(self):
        '''
        This test verifies that simple shifting works as expected,
        by checking that the result "final" load profile 
        is reduced from 8 to 6 in hour 15, and 
        is increased from 8 to 10.2 in hour 14.
        
        
        @author mstuebs
        @changed 2023-05-03
        '''
        enduse = 'EndUseName'
        day_slice = slice(0,24)

        demand = [8 for x in range(24)]
        demand_df = pd.DataFrame.from_dict({enduse: demand})

        price = [5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 8, 8, 8, 8]
        price_df = pd.DataFrame.from_dict({'Total': price})

        tech = {
            'rte': .9,
            'shift_window': 3,
            'base_load_frac': .25,
            'shift_direction': 'before',
        }
        shift_schedule = Basic_Shifter.get_shift_schedule(demand_df, day_slice, enduse, tech, price_df)
        
        assert shift_schedule.loc[13, 'final'] == 10.2
        assert shift_schedule.loc[14, 'final'] == 10.2
        assert shift_schedule.loc[15, 'final'] == 6.0
        assert shift_schedule.loc[16, 'final'] == 6.0
        
        
        cost_analysis = Basic_Shifter.do_cost_analysis(demand_df, shift_schedule, enduse, price_df)
        assert cost_analysis.iloc[-1]['Cost_Diff'] <= 0
         
          
    def test_shift_all(self):
        '''
        This test verifies that simple shifting works as expected,
        by checking that the result "final" load profile 
        is reduced from 8 to 6 in hour 15, and 
        is increased from 8 to 10.2 in hour 14.
        
        
        @author mstuebs
        @changed 2023-05-03
        '''
        enduse = 'EndUseName'
        day_slice = slice(0,24)

        demand = [8 for x in range(24)]
        demand_df = pd.DataFrame.from_dict({enduse: demand})

        price = [5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 5, 5, 5, 5, 5, 10, 10, 10, 10, 10, 8, 8, 8, 8]
        price_df = pd.DataFrame.from_dict({'Total': price})

        tech = {
            'rte': 1,
            'shift_window': 2,
            'base_load_frac': 1,
            'shift_direction': 'before',
        }
        shift_schedule = Basic_Shifter.get_shift_schedule(demand_df, day_slice, enduse, tech, price_df)
        assert shift_schedule.loc[13, 'final'] == 16
        assert shift_schedule.loc[14, 'final'] == 16
        assert shift_schedule.loc[15, 'final'] == 0
        assert shift_schedule.loc[16, 'final'] == 0
        cost_analysis = Basic_Shifter.do_cost_analysis(demand_df, shift_schedule, enduse, price_df)
        assert cost_analysis.iloc[-1]['Cost_Diff'] <= 0

    def test_only_one_cheap_hour(self):
        '''
        This test verifies that simple shifting works as expected,
        by introducing only one cheap hour
        and expecting that all load will be shifted there where possible

        @author mstuebs
        @changed 2023-05-03
        '''
        enduse = 'EndUseName'
        day_slice = slice(0,24)

        demand = [100]
        demand.extend([8 for x in range(23)])
        demand_df = pd.DataFrame.from_dict({enduse: demand})

        price = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 10, 9, 8, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        price_df = pd.DataFrame.from_dict({'Total': price})

        tech = {
            'rte': .5,
            'shift_window': 2,
            'base_load_frac': 1,
            'shift_direction': 'before',
        }
        shift_schedule = Basic_Shifter.get_shift_schedule(demand_df, day_slice, enduse, tech, price_df)
        #assert shift_schedule.loc[13, 'final'] == 16
        #assert shift_schedule.loc[14, 'final'] == 16
        #assert shift_schedule.loc[15, 'final'] == 0
        #assert shift_schedule.loc[16, 'final'] == 0
        cost_analysis = Basic_Shifter.do_cost_analysis(demand_df, shift_schedule, enduse, price_df)
        assert cost_analysis.iloc[-1]['Cost_Diff'] <= 0

    def test_shift_window_1(self):
        '''
        
        
        @author mstuebs
        @changed 2023-05-03
        '''
        enduse = 'EndUseName'
        day_slice = slice(0,24)

        demand = [8 for x in range(24)]
        demand_df = pd.DataFrame.from_dict({enduse: demand})

        price = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        price_df = pd.DataFrame.from_dict({'Total': price})

        tech = {
            'rte': 1,
            'shift_window': 2,
            'base_load_frac': 1,
            'shift_direction': 'before',
        }
        shift_schedule = Basic_Shifter.get_shift_schedule(demand_df, day_slice, enduse, tech, price_df)
        #assert shift_schedule.loc[13, 'final'] == 16
        #assert shift_schedule.loc[14, 'final'] == 16
        #assert shift_schedule.loc[15, 'final'] == 0
        #assert shift_schedule.loc[16, 'final'] == 0
        cost_analysis = Basic_Shifter.do_cost_analysis(demand_df, shift_schedule, enduse, price_df)
        assert cost_analysis.iloc[-1]['Cost_Diff'] <= 0
        
        
    def test_increasing_only_price(self):
        '''
        
        
        @author mstuebs
        @changed 2023-05-03
        '''
        enduse = 'EndUseName'
        day_slice = slice(0,24)

        demand = [8 for x in range(24)]
        demand_df = pd.DataFrame.from_dict({enduse: demand})

        price = [i for i in range(24)]
        price_df = pd.DataFrame.from_dict({'Total': price})

        tech = {
            'rte': 0.5,
            'shift_window': 3,
            'base_load_frac': 1,
            'shift_direction': 'before',
        }
        shift_schedule = Basic_Shifter.get_shift_schedule(demand_df, day_slice, enduse, tech, price_df)
        #assert shift_schedule.loc[13, 'final'] == 16
        #assert shift_schedule.loc[14, 'final'] == 16
        #assert shift_schedule.loc[15, 'final'] == 0
        #assert shift_schedule.loc[16, 'final'] == 0
        cost_analysis = Basic_Shifter.do_cost_analysis(demand_df, shift_schedule, enduse, price_df)
        assert cost_analysis.iloc[-1]['Cost_Diff'] <= 0
        
        
        
    def test_only_minimal_shift_window(self):
        '''
        This test verifies that simple shifting works as expected,
        by testing that if possible only neighboring hours shift
        and the shift window will not be maxed out

        @author mstuebs
        @changed 2023-05-03
        '''
        enduse = 'EndUseName'
        day_slice = slice(0,24)

        demand = [100]
        demand.extend([8 for x in range(23)])
        demand_df = pd.DataFrame.from_dict({enduse: demand})

        price = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 5, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        price_df = pd.DataFrame.from_dict({'Total': price})

        tech = {
            'rte': 1,
            'shift_window': 7,
            'base_load_frac': 1,
            'shift_direction': 'before',
        }
        shift_schedule = Basic_Shifter.get_shift_schedule(demand_df, day_slice, enduse, tech, price_df)
        #assert shift_schedule.loc[13, 'final'] == 16
        assert shift_schedule.loc[14, 'final'] == 16
        assert shift_schedule.loc[15, 'final'] == 0
        #assert shift_schedule.loc[16, 'final'] == 0
        cost_analysis = Basic_Shifter.do_cost_analysis(demand_df, shift_schedule, enduse, price_df)
        assert cost_analysis.iloc[-1]['Cost_Diff'] <= 0
