# coinglass_net_long_short
這是一個模擬 coingless 上面 net_long 和 net_short 指標計算的程式碼
滑動不同視窗時 coingless 後端會設定不同 start_time (如附檔的 py 程式碼) 而計算出不同的 net_long 和 net_short 數值
如果把視窗移到剛上架的合約 symbol 會發現 net_long + net_short = oi
