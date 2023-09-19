
class net_long_short:
    
    def __init__(
        self,
    ):
        pass
    
    def _fetch__oi(self, symbol, start_timestamp, end_timestamp , period):
        '''
        這個 function 用來拿取歷史 oi
        假設回傳 oi_dict = {timestamp1: oi1, timestamp2: oi2, ...}
        '''
        pass
    
    def _fetch_kline_close(self, symbol, start_timestamp, end_timestamp, period):
        '''
        這個 function 用來拿取歷史 kline 的 close
        假設回傳 price_dict = {timestamp1: close1, timestamp2: close2, ...}
        '''
        pass
    
    def net_long_short(
        self,
        symbol,
        start_timestamp,
        end_timestamp,
        period,
    ):
        '''
        timestamp_list 為一個 list,裡面包含了每個時間點
        從 start_timestamp 到 end_timestamp, 每隔 period 秒
        ex. 2023-09-19 00:00:00 ~ 2023-09-19 00:59:59 每五分鐘一個時間點
        [1695052800, 1695053100, 1695053400, 1695053700, 1695054000, 1695054300, 1695054600, 1695054900, 1695055200, 1695055500, 1695055800, 1695056100, 1695056400]
        
        目標算出 timestamp_list 上每個時間點的 net_long, net_short
        '''    
        
        # 先算出 timestamp_list
        timestamp_list = []
        current_timestamp = start_timestamp
        
        while current_timestamp <= end_timestamp:
            timestamp_list.append(current_timestamp)
            current_timestamp += period
        
        # 拿取 timestamp_list 上每個時間點的 oi 和價格變化
        oi_dict = self._fetch__oi(symbol, start_timestamp, end_timestamp, period)
        price_dict = self._fetch_kline_close(symbol, start_timestamp, end_timestamp, period)
        
        # 將開始時間的 net_long, net_short 設為 0
        net_long = {}
        net_short = {}
        net_long[start_timestamp] = 0
        net_short[start_timestamp] = 0
        
        for i in range(1,len(timestamp_list+1)):
            # 拿取 i+1 時間點和 i 時間點的 oi 和價格變化
            oi_delta = oi_dict[timestamp_list[i]] - oi_dict[timestamp_list[i-1]]
            price_delta = price_dict[timestamp_list[i]] - price_dict[timestamp_list[i-1]]
            
            # 如果價格變化為正且 oi 變化為正，則 net_long += abs(oi_delta)
            if price_delta > 0 and oi_delta > 0:
                net_long[timestamp_list[i]] = net_long[timestamp_list[i-1]] + oi_delta
                net_short[timestamp_list[i]] = net_short[timestamp_list[i-1]]
                
            # 如果價格變化為正且 oi 變化為負，則 net_short -= abs(oi_delta)
            if price_delta > 0 and oi_delta < 0:
                net_long[timestamp_list[i]] = net_long[timestamp_list[i-1]]
                net_short[timestamp_list[i]] = net_short[timestamp_list[i-1]] - abs(oi_delta)
            
            # 如果價格變化為負且 oi 變化為正，則 net_short += abs(oi_delta)
            if price_delta < 0 and oi_delta > 0:
                net_long[timestamp_list[i]] = net_long[timestamp_list[i-1]]
                net_short[timestamp_list[i]] = net_short[timestamp_list[i-1]] + abs(oi_delta)
            
            # 如果價格變化為負且 oi 變化為負，則 net_short -= abs(oi_delta)
            if price_delta < 0 and oi_delta < 0:
                net_long[timestamp_list[i]] = net_long[timestamp_list[i-1]] - abs(oi_delta)
                net_short[timestamp_list[i]] = net_short[timestamp_list[i-1]]
                
        return net_long, net_short
            
    