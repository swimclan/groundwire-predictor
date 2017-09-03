from Model import Model

class Observation(Model):
    def __init__(self, options={}):
        Model.__init__(self, options)

    def props(self):
        return [
            'id',
            'observed_datetime',
            'symbol',
            'num_new_highs',
            'num_new_lows',
            'num_highs_abv_avg_vol',
            'num_highs_blw_avg_vol',
            'num_lows_abv_avg_vol',
            'num_lows_blw_avg_vol',
            'num_new_highs_am',
            'num_new_highs_pm',
            'num_new_lows_am',
            'num_new_lows_pm',
            'percent_change',
            'tallest_green_candlestick',
            'tallest_red_candlestick',
            'age_recent_news',
            'market_open_datetime',
            'market_close_datetime',
            'next_market_open_margin'
        ]