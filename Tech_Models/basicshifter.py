import pandas as pd

class Basic_Shifter:
  def do_cost_analysis(demand_df, shift_schedule, enduse, price):
      cost_analysis = shift_schedule.copy()[['orig', 'take', 'final', 'shed', 'hour']]
      cost_analysis['shed'] = -1 * cost_analysis['shed']
      cost_analysis['Cost_Orig'] = cost_analysis['orig'] * price.loc[demand_df.index].reset_index()['Total']
      cost_analysis['Cost_Final'] = cost_analysis['final'] * price.loc[demand_df.index].reset_index()['Total']
      cost_analysis['Cost_Diff'] = cost_analysis['Cost_Final'].cumsum() - cost_analysis['Cost_Orig'].cumsum()
      cost_analysis['Load_Diff'] = cost_analysis['final'].cumsum() - cost_analysis['orig'].cumsum()
      return cost_analysis


  def weigh_possible_hours_to_shift_to(
          shed_hour: int, 
          possible_hours_to_shift_to, 
          schedule_orig: pd.DataFrame, 
          tech: dict, 
          prices: pd.DataFrame
  ):
    """
    @param shed_hour - The hour from where load shall be shifted
    @param possible_hours_to_shift_to - Pre-Selection of available hours
    @param schedule_orig - the complete load profile
    @param tech - To know how fast the take cools down
    @param prices - To know if the hours are really cheaper
    """
    ratings = {}
    for take_hour in possible_hours_to_shift_to:
        if take_hour < 0:
            continue
        distance = shed_hour - take_hour
        final_rte = (distance * (-1 * tech['rte']))
        
        
        price_difference = prices.loc[shed_hour, 'Total'] - prices.loc[take_hour, 'Total'] 
        
        
        rating = price_difference + final_rte
        
        if rating > 0:
            print(shed_hour, take_hour, "final_rte, price_difference", final_rte, price_difference, "rating", rating)
            ratings[take_hour] = rating
            #print("positive decision")
        else:
            pass
            #print("negative decision")
    
    #display("myratings", ratings)
    best_hours = sorted(ratings, key=ratings.get)  

    return best_hours
    

  '''
  Get shift schedule:
  
  This method takes in a load schedule and returns a load schedule
  that is optimized towards the price signal.
  
  @param schedule_orig - The original load schedule.
  @param day_slide - A slice representing the hours that can be shifted
  @param enduse - A strign
  @param tech - The parameters of the technology
   - RTE
   - base_load_frac
   - shift_window
  @param price - A price schedule
  
  @return shift_schedule: dict with the fields
          - 'orig'
          - 'shed'
          - 'take'
          - 'final'
  '''
  def get_shift_schedule(schedule_orig: pd.DataFrame, 
                         day_slice: slice, 
                         enduse: str, 
                         tech: dict,
                         price
                        ):
    shift_schedule = pd.DataFrame(0, index=schedule_orig.index, columns=['orig', 'shed', 'take', 'final'])
    for shed_hour in range(day_slice.stop - 1, day_slice.start - 1, -1):
        load_in_that_hour = schedule_orig.loc[shed_hour, enduse]
        sheddable_amount = tech['base_load_frac'] * load_in_that_hour
        ceil_take_amount = schedule_orig.loc[shed_hour, enduse].max()
        rte_factor = (1 + (1 - tech['rte']))

        shift_schedule.loc[shed_hour, 'orig'] = load_in_that_hour
        shift_schedule.loc[shed_hour, 'final'] = load_in_that_hour + shift_schedule.loc[shed_hour, 'take'] + shift_schedule.loc[shed_hour, 'shed']

        shed_price = price.loc[shed_hour, 'Total']
        
        possible_hours_to_shift_to = range(shed_hour - tech['shift_window'], shed_hour, 1)
        possible_hours_to_shift_to = Basic_Shifter.weigh_possible_hours_to_shift_to(shed_hour, possible_hours_to_shift_to, schedule_orig, tech, price)

        for take_hour in possible_hours_to_shift_to:
            take_hour += day_slice.start
            if take_hour < day_slice.start:
                continue
                
            take_price = price.loc[take_hour, 'Total']
            shift_schedule.loc[take_hour, 'orig'] = schedule_orig.loc[take_hour, enduse]
            
            
            #if shed_price > take_price:
                # go for it
                #print('Hour:', shed_hour)
                #print('Interval:', shift_interval)
                #print('Price difference:', shed_price, take_price, shed_price - take_price)

                
            shed_amount = -1 * sheddable_amount
            take_amount = sheddable_amount * rte_factor
            print(shed_hour, take_price, shed_amount, take_amount)

            has_ceiling = True
            if has_ceiling:
                if take_amount > ceil_take_amount - shift_schedule.loc[take_hour, 'take']:
                    print('ceil')
                    take_amount = ceil_take_amount - shift_schedule.loc[take_hour, 'take']
                    shed_amount = -1 * (take_amount / rte_factor)


            shift_schedule.loc[take_hour, 'take'] += take_amount
            shift_schedule.loc[shed_hour, 'shed'] += shed_amount

            shift_schedule.loc[take_hour, 'final'] += take_amount
            shift_schedule.loc[shed_hour, 'final'] += shed_amount

            #plot_current_action(schedule_orig, shift_schedule, enduse, take_hour, shed_hour, price)

    shift_schedule = shift_schedule.reset_index()
    shift_schedule = shift_schedule.rename(columns={'index': 'hour'})
    return shift_schedule