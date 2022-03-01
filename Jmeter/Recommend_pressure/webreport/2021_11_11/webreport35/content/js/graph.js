/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
$(document).ready(function() {

    $(".click-title").mouseenter( function(    e){
        e.preventDefault();
        this.style.cursor="pointer";
    });
    $(".click-title").mousedown( function(event){
        event.preventDefault();
    });

    // Ugly code while this script is shared among several pages
    try{
        refreshHitsPerSecond(true);
    } catch(e){}
    try{
        refreshResponseTimeOverTime(true);
    } catch(e){}
    try{
        refreshResponseTimePercentiles();
    } catch(e){}
});


var responseTimePercentilesInfos = {
        data: {"result": {"minY": 3205.0, "minX": 0.0, "maxY": 24085.0, "series": [{"data": [[0.0, 3205.0], [0.1, 3256.0], [0.2, 3311.0], [0.3, 3353.0], [0.4, 3715.0], [0.5, 4128.0], [0.6, 4377.0], [0.7, 4584.0], [0.8, 4616.0], [0.9, 4748.0], [1.0, 4919.0], [1.1, 4921.0], [1.2, 5157.0], [1.3, 5270.0], [1.4, 5474.0], [1.5, 5661.0], [1.6, 5741.0], [1.7, 5760.0], [1.8, 5972.0], [1.9, 6263.0], [2.0, 6292.0], [2.1, 6433.0], [2.2, 6587.0], [2.3, 6659.0], [2.4, 6710.0], [2.5, 6827.0], [2.6, 6895.0], [2.7, 6918.0], [2.8, 6958.0], [2.9, 7074.0], [3.0, 7114.0], [3.1, 7133.0], [3.2, 7270.0], [3.3, 7349.0], [3.4, 7371.0], [3.5, 7628.0], [3.6, 7649.0], [3.7, 7674.0], [3.8, 7744.0], [3.9, 7886.0], [4.0, 7966.0], [4.1, 7999.0], [4.2, 8014.0], [4.3, 8058.0], [4.4, 8064.0], [4.5, 8113.0], [4.6, 8130.0], [4.7, 8187.0], [4.8, 8212.0], [4.9, 8234.0], [5.0, 8278.0], [5.1, 8301.0], [5.2, 8377.0], [5.3, 8392.0], [5.4, 8421.0], [5.5, 8515.0], [5.6, 8533.0], [5.7, 8600.0], [5.8, 8626.0], [5.9, 8635.0], [6.0, 8709.0], [6.1, 8741.0], [6.2, 8793.0], [6.3, 8818.0], [6.4, 8819.0], [6.5, 8924.0], [6.6, 8947.0], [6.7, 8982.0], [6.8, 9023.0], [6.9, 9058.0], [7.0, 9134.0], [7.1, 9196.0], [7.2, 9209.0], [7.3, 9252.0], [7.4, 9298.0], [7.5, 9339.0], [7.6, 9343.0], [7.7, 9347.0], [7.8, 9381.0], [7.9, 9385.0], [8.0, 9401.0], [8.1, 9438.0], [8.2, 9474.0], [8.3, 9483.0], [8.4, 9507.0], [8.5, 9555.0], [8.6, 9565.0], [8.7, 9576.0], [8.8, 9587.0], [8.9, 9593.0], [9.0, 9611.0], [9.1, 9625.0], [9.2, 9634.0], [9.3, 9653.0], [9.4, 9686.0], [9.5, 9701.0], [9.6, 9710.0], [9.7, 9745.0], [9.8, 9759.0], [9.9, 9766.0], [10.0, 9767.0], [10.1, 9779.0], [10.2, 9791.0], [10.3, 9806.0], [10.4, 9820.0], [10.5, 9826.0], [10.6, 9861.0], [10.7, 9869.0], [10.8, 9876.0], [10.9, 9903.0], [11.0, 9905.0], [11.1, 9943.0], [11.2, 9950.0], [11.3, 9958.0], [11.4, 9969.0], [11.5, 10001.0], [11.6, 10021.0], [11.7, 10045.0], [11.8, 10056.0], [11.9, 10067.0], [12.0, 10079.0], [12.1, 10092.0], [12.2, 10119.0], [12.3, 10134.0], [12.4, 10147.0], [12.5, 10161.0], [12.6, 10168.0], [12.7, 10172.0], [12.8, 10187.0], [12.9, 10196.0], [13.0, 10209.0], [13.1, 10228.0], [13.2, 10255.0], [13.3, 10260.0], [13.4, 10269.0], [13.5, 10281.0], [13.6, 10285.0], [13.7, 10308.0], [13.8, 10312.0], [13.9, 10326.0], [14.0, 10348.0], [14.1, 10358.0], [14.2, 10364.0], [14.3, 10368.0], [14.4, 10391.0], [14.5, 10449.0], [14.6, 10469.0], [14.7, 10475.0], [14.8, 10486.0], [14.9, 10494.0], [15.0, 10500.0], [15.1, 10509.0], [15.2, 10515.0], [15.3, 10517.0], [15.4, 10531.0], [15.5, 10550.0], [15.6, 10566.0], [15.7, 10573.0], [15.8, 10579.0], [15.9, 10588.0], [16.0, 10600.0], [16.1, 10603.0], [16.2, 10619.0], [16.3, 10619.0], [16.4, 10650.0], [16.5, 10664.0], [16.6, 10670.0], [16.7, 10670.0], [16.8, 10675.0], [16.9, 10697.0], [17.0, 10704.0], [17.1, 10707.0], [17.2, 10725.0], [17.3, 10732.0], [17.4, 10741.0], [17.5, 10741.0], [17.6, 10754.0], [17.7, 10756.0], [17.8, 10759.0], [17.9, 10761.0], [18.0, 10766.0], [18.1, 10766.0], [18.2, 10772.0], [18.3, 10772.0], [18.4, 10778.0], [18.5, 10788.0], [18.6, 10802.0], [18.7, 10803.0], [18.8, 10809.0], [18.9, 10811.0], [19.0, 10817.0], [19.1, 10818.0], [19.2, 10830.0], [19.3, 10831.0], [19.4, 10833.0], [19.5, 10836.0], [19.6, 10845.0], [19.7, 10849.0], [19.8, 10852.0], [19.9, 10853.0], [20.0, 10858.0], [20.1, 10887.0], [20.2, 10900.0], [20.3, 10902.0], [20.4, 10913.0], [20.5, 10926.0], [20.6, 10931.0], [20.7, 10931.0], [20.8, 10940.0], [20.9, 10962.0], [21.0, 10965.0], [21.1, 10966.0], [21.2, 10971.0], [21.3, 10984.0], [21.4, 10998.0], [21.5, 10999.0], [21.6, 11001.0], [21.7, 11004.0], [21.8, 11010.0], [21.9, 11034.0], [22.0, 11040.0], [22.1, 11046.0], [22.2, 11049.0], [22.3, 11051.0], [22.4, 11056.0], [22.5, 11066.0], [22.6, 11078.0], [22.7, 11080.0], [22.8, 11084.0], [22.9, 11092.0], [23.0, 11097.0], [23.1, 11098.0], [23.2, 11103.0], [23.3, 11106.0], [23.4, 11109.0], [23.5, 11111.0], [23.6, 11114.0], [23.7, 11117.0], [23.8, 11122.0], [23.9, 11124.0], [24.0, 11131.0], [24.1, 11135.0], [24.2, 11138.0], [24.3, 11141.0], [24.4, 11144.0], [24.5, 11157.0], [24.6, 11168.0], [24.7, 11173.0], [24.8, 11176.0], [24.9, 11183.0], [25.0, 11188.0], [25.1, 11189.0], [25.2, 11197.0], [25.3, 11201.0], [25.4, 11201.0], [25.5, 11204.0], [25.6, 11213.0], [25.7, 11216.0], [25.8, 11218.0], [25.9, 11224.0], [26.0, 11225.0], [26.1, 11230.0], [26.2, 11239.0], [26.3, 11243.0], [26.4, 11250.0], [26.5, 11254.0], [26.6, 11254.0], [26.7, 11257.0], [26.8, 11266.0], [26.9, 11280.0], [27.0, 11281.0], [27.1, 11293.0], [27.2, 11300.0], [27.3, 11304.0], [27.4, 11305.0], [27.5, 11314.0], [27.6, 11317.0], [27.7, 11319.0], [27.8, 11321.0], [27.9, 11322.0], [28.0, 11324.0], [28.1, 11331.0], [28.2, 11332.0], [28.3, 11333.0], [28.4, 11348.0], [28.5, 11360.0], [28.6, 11361.0], [28.7, 11364.0], [28.8, 11366.0], [28.9, 11367.0], [29.0, 11369.0], [29.1, 11379.0], [29.2, 11385.0], [29.3, 11391.0], [29.4, 11392.0], [29.5, 11400.0], [29.6, 11404.0], [29.7, 11408.0], [29.8, 11409.0], [29.9, 11411.0], [30.0, 11415.0], [30.1, 11417.0], [30.2, 11419.0], [30.3, 11425.0], [30.4, 11429.0], [30.5, 11435.0], [30.6, 11435.0], [30.7, 11450.0], [30.8, 11461.0], [30.9, 11465.0], [31.0, 11467.0], [31.1, 11475.0], [31.2, 11478.0], [31.3, 11482.0], [31.4, 11482.0], [31.5, 11487.0], [31.6, 11490.0], [31.7, 11503.0], [31.8, 11505.0], [31.9, 11517.0], [32.0, 11519.0], [32.1, 11520.0], [32.2, 11521.0], [32.3, 11525.0], [32.4, 11529.0], [32.5, 11532.0], [32.6, 11537.0], [32.7, 11544.0], [32.8, 11549.0], [32.9, 11551.0], [33.0, 11552.0], [33.1, 11554.0], [33.2, 11559.0], [33.3, 11561.0], [33.4, 11564.0], [33.5, 11575.0], [33.6, 11577.0], [33.7, 11585.0], [33.8, 11585.0], [33.9, 11587.0], [34.0, 11593.0], [34.1, 11595.0], [34.2, 11600.0], [34.3, 11606.0], [34.4, 11613.0], [34.5, 11621.0], [34.6, 11632.0], [34.7, 11633.0], [34.8, 11635.0], [34.9, 11636.0], [35.0, 11637.0], [35.1, 11645.0], [35.2, 11649.0], [35.3, 11650.0], [35.4, 11653.0], [35.5, 11657.0], [35.6, 11661.0], [35.7, 11667.0], [35.8, 11667.0], [35.9, 11670.0], [36.0, 11673.0], [36.1, 11677.0], [36.2, 11681.0], [36.3, 11682.0], [36.4, 11684.0], [36.5, 11687.0], [36.6, 11691.0], [36.7, 11694.0], [36.8, 11696.0], [36.9, 11706.0], [37.0, 11710.0], [37.1, 11716.0], [37.2, 11724.0], [37.3, 11728.0], [37.4, 11733.0], [37.5, 11734.0], [37.6, 11742.0], [37.7, 11743.0], [37.8, 11743.0], [37.9, 11744.0], [38.0, 11751.0], [38.1, 11756.0], [38.2, 11759.0], [38.3, 11766.0], [38.4, 11768.0], [38.5, 11779.0], [38.6, 11782.0], [38.7, 11789.0], [38.8, 11792.0], [38.9, 11793.0], [39.0, 11794.0], [39.1, 11798.0], [39.2, 11803.0], [39.3, 11809.0], [39.4, 11817.0], [39.5, 11822.0], [39.6, 11823.0], [39.7, 11823.0], [39.8, 11825.0], [39.9, 11837.0], [40.0, 11839.0], [40.1, 11840.0], [40.2, 11850.0], [40.3, 11853.0], [40.4, 11857.0], [40.5, 11857.0], [40.6, 11863.0], [40.7, 11866.0], [40.8, 11868.0], [40.9, 11870.0], [41.0, 11871.0], [41.1, 11877.0], [41.2, 11879.0], [41.3, 11880.0], [41.4, 11883.0], [41.5, 11888.0], [41.6, 11892.0], [41.7, 11894.0], [41.8, 11895.0], [41.9, 11900.0], [42.0, 11902.0], [42.1, 11902.0], [42.2, 11903.0], [42.3, 11908.0], [42.4, 11917.0], [42.5, 11922.0], [42.6, 11923.0], [42.7, 11927.0], [42.8, 11937.0], [42.9, 11939.0], [43.0, 11942.0], [43.1, 11946.0], [43.2, 11949.0], [43.3, 11950.0], [43.4, 11952.0], [43.5, 11953.0], [43.6, 11957.0], [43.7, 11958.0], [43.8, 11963.0], [43.9, 11968.0], [44.0, 11969.0], [44.1, 11974.0], [44.2, 11993.0], [44.3, 11993.0], [44.4, 11995.0], [44.5, 11998.0], [44.6, 12003.0], [44.7, 12004.0], [44.8, 12004.0], [44.9, 12004.0], [45.0, 12009.0], [45.1, 12013.0], [45.2, 12019.0], [45.3, 12019.0], [45.4, 12021.0], [45.5, 12028.0], [45.6, 12034.0], [45.7, 12034.0], [45.8, 12036.0], [45.9, 12037.0], [46.0, 12047.0], [46.1, 12052.0], [46.2, 12056.0], [46.3, 12057.0], [46.4, 12059.0], [46.5, 12059.0], [46.6, 12063.0], [46.7, 12068.0], [46.8, 12073.0], [46.9, 12076.0], [47.0, 12081.0], [47.1, 12084.0], [47.2, 12084.0], [47.3, 12088.0], [47.4, 12089.0], [47.5, 12094.0], [47.6, 12098.0], [47.7, 12098.0], [47.8, 12099.0], [47.9, 12101.0], [48.0, 12108.0], [48.1, 12109.0], [48.2, 12114.0], [48.3, 12123.0], [48.4, 12125.0], [48.5, 12126.0], [48.6, 12128.0], [48.7, 12132.0], [48.8, 12134.0], [48.9, 12134.0], [49.0, 12136.0], [49.1, 12137.0], [49.2, 12140.0], [49.3, 12142.0], [49.4, 12144.0], [49.5, 12149.0], [49.6, 12153.0], [49.7, 12154.0], [49.8, 12156.0], [49.9, 12164.0], [50.0, 12165.0], [50.1, 12166.0], [50.2, 12168.0], [50.3, 12169.0], [50.4, 12170.0], [50.5, 12175.0], [50.6, 12181.0], [50.7, 12194.0], [50.8, 12195.0], [50.9, 12206.0], [51.0, 12208.0], [51.1, 12215.0], [51.2, 12215.0], [51.3, 12218.0], [51.4, 12219.0], [51.5, 12222.0], [51.6, 12224.0], [51.7, 12228.0], [51.8, 12233.0], [51.9, 12242.0], [52.0, 12242.0], [52.1, 12246.0], [52.2, 12254.0], [52.3, 12256.0], [52.4, 12256.0], [52.5, 12260.0], [52.6, 12263.0], [52.7, 12266.0], [52.8, 12266.0], [52.9, 12270.0], [53.0, 12272.0], [53.1, 12272.0], [53.2, 12272.0], [53.3, 12275.0], [53.4, 12279.0], [53.5, 12282.0], [53.6, 12284.0], [53.7, 12285.0], [53.8, 12286.0], [53.9, 12288.0], [54.0, 12291.0], [54.1, 12300.0], [54.2, 12305.0], [54.3, 12307.0], [54.4, 12307.0], [54.5, 12325.0], [54.6, 12327.0], [54.7, 12329.0], [54.8, 12332.0], [54.9, 12339.0], [55.0, 12344.0], [55.1, 12345.0], [55.2, 12352.0], [55.3, 12358.0], [55.4, 12361.0], [55.5, 12364.0], [55.6, 12365.0], [55.7, 12367.0], [55.8, 12369.0], [55.9, 12372.0], [56.0, 12373.0], [56.1, 12377.0], [56.2, 12388.0], [56.3, 12388.0], [56.4, 12389.0], [56.5, 12396.0], [56.6, 12400.0], [56.7, 12401.0], [56.8, 12402.0], [56.9, 12404.0], [57.0, 12405.0], [57.1, 12409.0], [57.2, 12410.0], [57.3, 12412.0], [57.4, 12415.0], [57.5, 12416.0], [57.6, 12417.0], [57.7, 12425.0], [57.8, 12427.0], [57.9, 12437.0], [58.0, 12437.0], [58.1, 12439.0], [58.2, 12443.0], [58.3, 12451.0], [58.4, 12457.0], [58.5, 12458.0], [58.6, 12462.0], [58.7, 12465.0], [58.8, 12465.0], [58.9, 12469.0], [59.0, 12475.0], [59.1, 12479.0], [59.2, 12480.0], [59.3, 12483.0], [59.4, 12484.0], [59.5, 12487.0], [59.6, 12487.0], [59.7, 12491.0], [59.8, 12492.0], [59.9, 12493.0], [60.0, 12493.0], [60.1, 12496.0], [60.2, 12499.0], [60.3, 12502.0], [60.4, 12503.0], [60.5, 12504.0], [60.6, 12505.0], [60.7, 12510.0], [60.8, 12510.0], [60.9, 12512.0], [61.0, 12516.0], [61.1, 12524.0], [61.2, 12528.0], [61.3, 12534.0], [61.4, 12539.0], [61.5, 12540.0], [61.6, 12540.0], [61.7, 12545.0], [61.8, 12552.0], [61.9, 12554.0], [62.0, 12554.0], [62.1, 12557.0], [62.2, 12562.0], [62.3, 12564.0], [62.4, 12565.0], [62.5, 12568.0], [62.6, 12573.0], [62.7, 12575.0], [62.8, 12578.0], [62.9, 12579.0], [63.0, 12590.0], [63.1, 12591.0], [63.2, 12594.0], [63.3, 12599.0], [63.4, 12604.0], [63.5, 12604.0], [63.6, 12621.0], [63.7, 12624.0], [63.8, 12630.0], [63.9, 12631.0], [64.0, 12633.0], [64.1, 12639.0], [64.2, 12648.0], [64.3, 12648.0], [64.4, 12655.0], [64.5, 12658.0], [64.6, 12659.0], [64.7, 12659.0], [64.8, 12664.0], [64.9, 12668.0], [65.0, 12673.0], [65.1, 12675.0], [65.2, 12679.0], [65.3, 12682.0], [65.4, 12683.0], [65.5, 12684.0], [65.6, 12687.0], [65.7, 12691.0], [65.8, 12694.0], [65.9, 12697.0], [66.0, 12703.0], [66.1, 12707.0], [66.2, 12707.0], [66.3, 12710.0], [66.4, 12711.0], [66.5, 12714.0], [66.6, 12719.0], [66.7, 12721.0], [66.8, 12723.0], [66.9, 12727.0], [67.0, 12732.0], [67.1, 12733.0], [67.2, 12742.0], [67.3, 12749.0], [67.4, 12750.0], [67.5, 12751.0], [67.6, 12755.0], [67.7, 12767.0], [67.8, 12769.0], [67.9, 12771.0], [68.0, 12776.0], [68.1, 12779.0], [68.2, 12784.0], [68.3, 12786.0], [68.4, 12791.0], [68.5, 12793.0], [68.6, 12799.0], [68.7, 12800.0], [68.8, 12806.0], [68.9, 12806.0], [69.0, 12813.0], [69.1, 12813.0], [69.2, 12815.0], [69.3, 12820.0], [69.4, 12824.0], [69.5, 12829.0], [69.6, 12836.0], [69.7, 12839.0], [69.8, 12842.0], [69.9, 12844.0], [70.0, 12846.0], [70.1, 12858.0], [70.2, 12861.0], [70.3, 12867.0], [70.4, 12876.0], [70.5, 12877.0], [70.6, 12880.0], [70.7, 12889.0], [70.8, 12898.0], [70.9, 12902.0], [71.0, 12918.0], [71.1, 12918.0], [71.2, 12925.0], [71.3, 12931.0], [71.4, 12936.0], [71.5, 12936.0], [71.6, 12943.0], [71.7, 12946.0], [71.8, 12951.0], [71.9, 12954.0], [72.0, 12959.0], [72.1, 12964.0], [72.2, 12965.0], [72.3, 12973.0], [72.4, 12974.0], [72.5, 12980.0], [72.6, 12991.0], [72.7, 12992.0], [72.8, 12998.0], [72.9, 13003.0], [73.0, 13005.0], [73.1, 13009.0], [73.2, 13012.0], [73.3, 13018.0], [73.4, 13019.0], [73.5, 13027.0], [73.6, 13032.0], [73.7, 13035.0], [73.8, 13041.0], [73.9, 13043.0], [74.0, 13048.0], [74.1, 13059.0], [74.2, 13061.0], [74.3, 13062.0], [74.4, 13078.0], [74.5, 13085.0], [74.6, 13098.0], [74.7, 13100.0], [74.8, 13108.0], [74.9, 13114.0], [75.0, 13115.0], [75.1, 13117.0], [75.2, 13123.0], [75.3, 13138.0], [75.4, 13138.0], [75.5, 13140.0], [75.6, 13141.0], [75.7, 13155.0], [75.8, 13157.0], [75.9, 13164.0], [76.0, 13177.0], [76.1, 13206.0], [76.2, 13211.0], [76.3, 13212.0], [76.4, 13216.0], [76.5, 13224.0], [76.6, 13224.0], [76.7, 13231.0], [76.8, 13252.0], [76.9, 13269.0], [77.0, 13275.0], [77.1, 13284.0], [77.2, 13289.0], [77.3, 13305.0], [77.4, 13307.0], [77.5, 13308.0], [77.6, 13309.0], [77.7, 13311.0], [77.8, 13324.0], [77.9, 13325.0], [78.0, 13339.0], [78.1, 13340.0], [78.2, 13344.0], [78.3, 13347.0], [78.4, 13369.0], [78.5, 13374.0], [78.6, 13376.0], [78.7, 13388.0], [78.8, 13398.0], [78.9, 13402.0], [79.0, 13407.0], [79.1, 13414.0], [79.2, 13418.0], [79.3, 13420.0], [79.4, 13421.0], [79.5, 13422.0], [79.6, 13449.0], [79.7, 13460.0], [79.8, 13469.0], [79.9, 13479.0], [80.0, 13486.0], [80.1, 13492.0], [80.2, 13507.0], [80.3, 13512.0], [80.4, 13532.0], [80.5, 13547.0], [80.6, 13562.0], [80.7, 13565.0], [80.8, 13575.0], [80.9, 13588.0], [81.0, 13590.0], [81.1, 13603.0], [81.2, 13616.0], [81.3, 13625.0], [81.4, 13626.0], [81.5, 13632.0], [81.6, 13652.0], [81.7, 13657.0], [81.8, 13660.0], [81.9, 13661.0], [82.0, 13670.0], [82.1, 13674.0], [82.2, 13683.0], [82.3, 13686.0], [82.4, 13689.0], [82.5, 13689.0], [82.6, 13692.0], [82.7, 13700.0], [82.8, 13737.0], [82.9, 13748.0], [83.0, 13749.0], [83.1, 13759.0], [83.2, 13768.0], [83.3, 13780.0], [83.4, 13782.0], [83.5, 13787.0], [83.6, 13794.0], [83.7, 13805.0], [83.8, 13809.0], [83.9, 13815.0], [84.0, 13829.0], [84.1, 13834.0], [84.2, 13840.0], [84.3, 13845.0], [84.4, 13851.0], [84.5, 13861.0], [84.6, 13884.0], [84.7, 13891.0], [84.8, 13916.0], [84.9, 13933.0], [85.0, 13941.0], [85.1, 13947.0], [85.2, 13952.0], [85.3, 13982.0], [85.4, 13988.0], [85.5, 13989.0], [85.6, 13998.0], [85.7, 14018.0], [85.8, 14019.0], [85.9, 14041.0], [86.0, 14050.0], [86.1, 14062.0], [86.2, 14064.0], [86.3, 14071.0], [86.4, 14092.0], [86.5, 14120.0], [86.6, 14128.0], [86.7, 14141.0], [86.8, 14158.0], [86.9, 14179.0], [87.0, 14179.0], [87.1, 14194.0], [87.2, 14230.0], [87.3, 14250.0], [87.4, 14253.0], [87.5, 14274.0], [87.6, 14286.0], [87.7, 14294.0], [87.8, 14299.0], [87.9, 14320.0], [88.0, 14331.0], [88.1, 14336.0], [88.2, 14354.0], [88.3, 14371.0], [88.4, 14380.0], [88.5, 14384.0], [88.6, 14392.0], [88.7, 14425.0], [88.8, 14440.0], [88.9, 14448.0], [89.0, 14483.0], [89.1, 14496.0], [89.2, 14497.0], [89.3, 14499.0], [89.4, 14515.0], [89.5, 14526.0], [89.6, 14551.0], [89.7, 14553.0], [89.8, 14557.0], [89.9, 14568.0], [90.0, 14576.0], [90.1, 14579.0], [90.2, 14622.0], [90.3, 14656.0], [90.4, 14665.0], [90.5, 14672.0], [90.6, 14675.0], [90.7, 14692.0], [90.8, 14711.0], [90.9, 14721.0], [91.0, 14745.0], [91.1, 14773.0], [91.2, 14789.0], [91.3, 14792.0], [91.4, 14808.0], [91.5, 14820.0], [91.6, 14837.0], [91.7, 14855.0], [91.8, 14865.0], [91.9, 14878.0], [92.0, 14890.0], [92.1, 14896.0], [92.2, 14928.0], [92.3, 14993.0], [92.4, 15013.0], [92.5, 15014.0], [92.6, 15022.0], [92.7, 15070.0], [92.8, 15098.0], [92.9, 15121.0], [93.0, 15148.0], [93.1, 15195.0], [93.2, 15211.0], [93.3, 15214.0], [93.4, 15225.0], [93.5, 15236.0], [93.6, 15262.0], [93.7, 15289.0], [93.8, 15309.0], [93.9, 15407.0], [94.0, 15416.0], [94.1, 15470.0], [94.2, 15494.0], [94.3, 15543.0], [94.4, 15598.0], [94.5, 15600.0], [94.6, 15641.0], [94.7, 15683.0], [94.8, 15760.0], [94.9, 15779.0], [95.0, 15799.0], [95.1, 15817.0], [95.2, 15849.0], [95.3, 15886.0], [95.4, 15992.0], [95.5, 16009.0], [95.6, 16035.0], [95.7, 16062.0], [95.8, 16110.0], [95.9, 16160.0], [96.0, 16170.0], [96.1, 16182.0], [96.2, 16227.0], [96.3, 16455.0], [96.4, 16507.0], [96.5, 16551.0], [96.6, 16628.0], [96.7, 16658.0], [96.8, 16713.0], [96.9, 16717.0], [97.0, 16801.0], [97.1, 16812.0], [97.2, 16948.0], [97.3, 17033.0], [97.4, 17114.0], [97.5, 17196.0], [97.6, 17205.0], [97.7, 17214.0], [97.8, 17333.0], [97.9, 17366.0], [98.0, 17507.0], [98.1, 17507.0], [98.2, 17617.0], [98.3, 17674.0], [98.4, 18054.0], [98.5, 18084.0], [98.6, 18239.0], [98.7, 18313.0], [98.8, 18658.0], [98.9, 18740.0], [99.0, 18925.0], [99.1, 19071.0], [99.2, 19154.0], [99.3, 19253.0], [99.4, 19812.0], [99.5, 20106.0], [99.6, 20227.0], [99.7, 20346.0], [99.8, 22566.0], [99.9, 24082.0], [100.0, 24085.0]], "isOverall": false, "label": "HTTP\u8BF7\u6C42", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 100.0, "title": "Response Time Percentiles"}},
        getOptions: function() {
            return {
                series: {
                    points: { show: false }
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentiles'
                },
                xaxis: {
                    tickDecimals: 1,
                    axisLabel: "Percentiles",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Percentile value in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : %x.2 percentile was %y ms"
                },
                selection: { mode: "xy" },
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentiles"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesPercentiles"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesPercentiles"), dataset, prepareOverviewOptions(options));
        }
};

/**
 * @param elementId Id of element where we display message
 */
function setEmptyGraph(elementId) {
    $(function() {
        $(elementId).text("No graph series with filter="+seriesFilter);
    });
}

// Response times percentiles
function refreshResponseTimePercentiles() {
    var infos = responseTimePercentilesInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimePercentiles");
        return;
    }
    if (isGraph($("#flotResponseTimesPercentiles"))){
        infos.createGraph();
    } else {
        var choiceContainer = $("#choicesResponseTimePercentiles");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesPercentiles", "#overviewResponseTimesPercentiles");
        $('#bodyResponseTimePercentiles .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimeDistributionInfos = {
        data: {"result": {"minY": 1.0, "minX": 3200.0, "maxY": 64.0, "series": [{"data": [[3200.0, 3.0], [3300.0, 3.0], [3700.0, 1.0], [4000.0, 1.0], [4300.0, 1.0], [4200.0, 1.0], [4100.0, 1.0], [4500.0, 1.0], [4600.0, 1.0], [4400.0, 1.0], [4700.0, 2.0], [4800.0, 1.0], [4900.0, 3.0], [5100.0, 1.0], [5200.0, 2.0], [5300.0, 1.0], [5600.0, 1.0], [5400.0, 1.0], [5500.0, 1.0], [5700.0, 3.0], [5800.0, 1.0], [5900.0, 1.0], [6200.0, 3.0], [6300.0, 1.0], [6500.0, 1.0], [6600.0, 2.0], [6400.0, 2.0], [6900.0, 2.0], [6700.0, 2.0], [6800.0, 4.0], [7000.0, 2.0], [7100.0, 4.0], [7200.0, 2.0], [7300.0, 3.0], [7400.0, 1.0], [7600.0, 4.0], [7700.0, 2.0], [7900.0, 3.0], [7800.0, 2.0], [8100.0, 5.0], [8000.0, 6.0], [8600.0, 5.0], [8500.0, 3.0], [8200.0, 6.0], [8700.0, 5.0], [8300.0, 4.0], [8400.0, 3.0], [8900.0, 5.0], [9200.0, 5.0], [8800.0, 4.0], [9000.0, 4.0], [9100.0, 3.0], [9400.0, 7.0], [9700.0, 14.0], [9600.0, 9.0], [9500.0, 10.0], [9300.0, 9.0], [10100.0, 13.0], [9900.0, 11.0], [10000.0, 12.0], [10200.0, 13.0], [9800.0, 11.0], [10600.0, 17.0], [10700.0, 29.0], [10400.0, 10.0], [10500.0, 17.0], [10300.0, 13.0], [10800.0, 28.0], [11000.0, 28.0], [11100.0, 37.0], [10900.0, 23.0], [11200.0, 34.0], [11300.0, 40.0], [11700.0, 39.0], [11400.0, 39.0], [11500.0, 43.0], [11600.0, 48.0], [12000.0, 58.0], [12200.0, 57.0], [12100.0, 52.0], [11900.0, 46.0], [11800.0, 48.0], [12600.0, 45.0], [12300.0, 44.0], [12400.0, 64.0], [12500.0, 54.0], [12700.0, 48.0], [12900.0, 35.0], [13200.0, 21.0], [13000.0, 32.0], [13300.0, 27.0], [12800.0, 38.0], [13100.0, 25.0], [13400.0, 23.0], [13700.0, 18.0], [13800.0, 18.0], [13600.0, 29.0], [13500.0, 15.0], [14200.0, 12.0], [13900.0, 16.0], [14300.0, 14.0], [14100.0, 12.0], [14000.0, 14.0], [14600.0, 12.0], [14800.0, 14.0], [14700.0, 10.0], [14500.0, 14.0], [14400.0, 12.0], [15000.0, 9.0], [15200.0, 11.0], [14900.0, 3.0], [15100.0, 5.0], [15300.0, 2.0], [15700.0, 5.0], [15400.0, 7.0], [15600.0, 5.0], [15800.0, 5.0], [15500.0, 3.0], [16100.0, 8.0], [15900.0, 3.0], [16200.0, 1.0], [16000.0, 4.0], [17200.0, 3.0], [16800.0, 3.0], [16700.0, 3.0], [16600.0, 4.0], [17300.0, 3.0], [16500.0, 3.0], [17100.0, 4.0], [16900.0, 2.0], [17000.0, 2.0], [16400.0, 3.0], [17400.0, 1.0], [18000.0, 2.0], [17600.0, 3.0], [18100.0, 1.0], [17800.0, 1.0], [18200.0, 2.0], [18400.0, 1.0], [17500.0, 3.0], [18300.0, 1.0], [19200.0, 1.0], [19000.0, 3.0], [18700.0, 1.0], [18800.0, 1.0], [19100.0, 1.0], [18900.0, 1.0], [18600.0, 1.0], [19300.0, 1.0], [20200.0, 2.0], [19800.0, 2.0], [20300.0, 1.0], [20100.0, 1.0], [20700.0, 1.0], [22500.0, 1.0], [22600.0, 1.0], [24000.0, 2.0]], "isOverall": false, "label": "HTTP\u8BF7\u6C42", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 100, "maxX": 24000.0, "title": "Response Time Distribution"}},
        getOptions: function() {
            var granularity = this.data.result.granularity;
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    barWidth: this.data.result.granularity
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " responses for " + label + " were between " + xval + " and " + (xval + granularity) + " ms";
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimeDistribution"), prepareData(data.result.series, $("#choicesResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshResponseTimeDistribution() {
    var infos = responseTimeDistributionInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeDistribution");
        return;
    }
    if (isGraph($("#flotResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var syntheticResponseTimeDistributionInfos = {
        data: {"result": {"minY": 1748.0, "minX": 2.0, "ticks": [[0, "Requests having \nresponse time <= 500ms"], [1, "Requests having \nresponse time > 500ms and <= 1,500ms"], [2, "Requests having \nresponse time > 1,500ms"], [3, "Requests in error"]], "maxY": 1748.0, "series": [{"data": [], "color": "#9ACD32", "isOverall": false, "label": "Requests having \nresponse time <= 500ms", "isController": false}, {"data": [], "color": "yellow", "isOverall": false, "label": "Requests having \nresponse time > 500ms and <= 1,500ms", "isController": false}, {"data": [[2.0, 1748.0]], "color": "orange", "isOverall": false, "label": "Requests having \nresponse time > 1,500ms", "isController": false}, {"data": [], "color": "#FF6347", "isOverall": false, "label": "Requests in error", "isController": false}], "supportsControllersDiscrimination": false, "maxX": 2.0, "title": "Synthetic Response Times Distribution"}},
        getOptions: function() {
            return {
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendSyntheticResponseTimeDistribution'
                },
                xaxis:{
                    axisLabel: "Response times ranges",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                    tickLength:0,
                    min:-0.5,
                    max:3.5
                },
                yaxis: {
                    axisLabel: "Number of responses",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                bars : {
                    show: true,
                    align: "center",
                    barWidth: 0.25,
                    fill:.75
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: function(label, xval, yval, flotItem){
                        return yval + " " + label;
                    }
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var options = this.getOptions();
            prepareOptions(options, data);
            options.xaxis.ticks = data.result.ticks;
            $.plot($("#flotSyntheticResponseTimeDistribution"), prepareData(data.result.series, $("#choicesSyntheticResponseTimeDistribution")), options);
        }

};

// Response time distribution
function refreshSyntheticResponseTimeDistribution() {
    var infos = syntheticResponseTimeDistributionInfos;
    prepareSeries(infos.data, true);
    if (isGraph($("#flotSyntheticResponseTimeDistribution"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        $('#footerSyntheticResponseTimeDistribution .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var activeThreadsOverTimeInfos = {
        data: {"result": {"minY": 20.833333333333332, "minX": 1.63607658E12, "maxY": 35.0, "series": [{"data": [[1.63607658E12, 35.0], [1.63607706E12, 35.0], [1.63607688E12, 35.0], [1.63607694E12, 35.0], [1.63607676E12, 35.0], [1.63607682E12, 35.0], [1.63607664E12, 35.0], [1.63607712E12, 35.0], [1.6360767E12, 35.0], [1.63607718E12, 20.833333333333332], [1.636077E12, 35.0]], "isOverall": false, "label": "\u7EBF\u7A0B\u7EC4", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.63607718E12, "title": "Active Threads Over Time"}},
        getOptions: function() {
            return {
                series: {
                    stack: true,
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 6,
                    show: true,
                    container: '#legendActiveThreadsOverTime'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                selection: {
                    mode: 'xy'
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : At %x there were %y active threads"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesActiveThreadsOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotActiveThreadsOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewActiveThreadsOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Active Threads Over Time
function refreshActiveThreadsOverTime(fixTimestamps) {
    var infos = activeThreadsOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotActiveThreadsOverTime"))) {
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesActiveThreadsOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotActiveThreadsOverTime", "#overviewActiveThreadsOverTime");
        $('#footerActiveThreadsOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var timeVsThreadsInfos = {
        data: {"result": {"minY": 11229.0, "minX": 1.0, "maxY": 17507.0, "series": [{"data": [[33.0, 11666.0], [32.0, 11319.0], [2.0, 17043.0], [35.0, 12136.051341890308], [34.0, 12552.0], [3.0, 15494.0], [4.0, 12800.0], [5.0, 12839.0], [6.0, 12991.0], [7.0, 13373.0], [8.0, 12510.0], [9.0, 12948.0], [10.0, 13041.0], [11.0, 13369.0], [12.0, 12244.0], [13.0, 13295.0], [14.0, 14568.0], [15.0, 13697.0], [16.0, 14331.0], [1.0, 17507.0], [17.0, 11229.0], [18.0, 11885.0], [19.0, 13400.0], [20.0, 11519.0], [21.0, 12109.0], [22.0, 12133.0], [23.0, 12733.0], [24.0, 11490.0], [25.0, 11531.0], [26.0, 11759.0], [27.0, 13275.0], [28.0, 13815.0], [29.0, 11521.0], [30.0, 13224.0], [31.0, 13114.0]], "isOverall": false, "label": "HTTP\u8BF7\u6C42", "isController": false}, {"data": [[34.65961098398168, 12153.041189931344]], "isOverall": false, "label": "HTTP\u8BF7\u6C42-Aggregated", "isController": false}], "supportsControllersDiscrimination": true, "maxX": 35.0, "title": "Time VS Threads"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    axisLabel: "Number of active threads",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response times in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: { noColumns: 2,show: true, container: '#legendTimeVsThreads' },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s: At %x.2 active threads, Average response time was %y.2 ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesTimeVsThreads"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotTimesVsThreads"), dataset, options);
            // setup overview
            $.plot($("#overviewTimesVsThreads"), dataset, prepareOverviewOptions(options));
        }
};

// Time vs threads
function refreshTimeVsThreads(){
    var infos = timeVsThreadsInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTimeVsThreads");
        return;
    }
    if(isGraph($("#flotTimesVsThreads"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTimeVsThreads");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTimesVsThreads", "#overviewTimesVsThreads");
        $('#footerTimeVsThreads .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var bytesThroughputOverTimeInfos = {
        data : {"result": {"minY": 167.3, "minX": 1.63607658E12, "maxY": 88214.43333333333, "series": [{"data": [[1.63607658E12, 81223.03333333334], [1.63607706E12, 81708.1], [1.63607688E12, 81873.96666666666], [1.63607694E12, 82779.06666666667], [1.63607676E12, 81879.46666666666], [1.63607682E12, 82646.46666666666], [1.63607664E12, 85160.56666666667], [1.63607712E12, 82717.25], [1.6360767E12, 88214.43333333333], [1.63607718E12, 20462.35], [1.636077E12, 82321.65]], "isOverall": false, "label": "Bytes received per second", "isController": false}, {"data": [[1.63607658E12, 665.2166666666667], [1.63607706E12, 669.2], [1.63607688E12, 669.2], [1.63607694E12, 677.1666666666666], [1.63607676E12, 669.2], [1.63607682E12, 677.1666666666666], [1.63607664E12, 697.0833333333334], [1.63607712E12, 677.1666666666666], [1.6360767E12, 720.9833333333333], [1.63607718E12, 167.3], [1.636077E12, 673.1833333333333]], "isOverall": false, "label": "Bytes sent per second", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.63607718E12, "title": "Bytes Throughput Over Time"}},
        getOptions : function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity) ,
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Bytes / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendBytesThroughputOverTime'
                },
                selection: {
                    mode: "xy"
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y"
                }
            };
        },
        createGraph : function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesBytesThroughputOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotBytesThroughputOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewBytesThroughputOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Bytes throughput Over Time
function refreshBytesThroughputOverTime(fixTimestamps) {
    var infos = bytesThroughputOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotBytesThroughputOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesBytesThroughputOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotBytesThroughputOverTime", "#overviewBytesThroughputOverTime");
        $('#footerBytesThroughputOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var responseTimesOverTimeInfos = {
        data: {"result": {"minY": 10668.94610778443, "minX": 1.63607658E12, "maxY": 12916.761904761897, "series": [{"data": [[1.63607658E12, 10668.94610778443], [1.63607706E12, 12297.065476190475], [1.63607688E12, 12384.904761904761], [1.63607694E12, 12511.205882352937], [1.63607676E12, 12373.892857142859], [1.63607682E12, 12367.741176470583], [1.63607664E12, 11852.085714285715], [1.63607712E12, 12576.376470588228], [1.6360767E12, 11927.651933701662], [1.63607718E12, 12916.761904761897], [1.636077E12, 12387.502958579882]], "isOverall": false, "label": "HTTP\u8BF7\u6C42", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.63607718E12, "title": "Response Time Over Time"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average response time was %y ms"
                }
            };
        },
        createGraph: function() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Times Over Time
function refreshResponseTimeOverTime(fixTimestamps) {
    var infos = responseTimesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyResponseTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotResponseTimesOverTime"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimesOverTime", "#overviewResponseTimesOverTime");
        $('#footerResponseTimesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var latenciesOverTimeInfos = {
        data: {"result": {"minY": 10662.730538922162, "minX": 1.63607658E12, "maxY": 12910.023809523811, "series": [{"data": [[1.63607658E12, 10662.730538922162], [1.63607706E12, 12290.54761904762], [1.63607688E12, 12376.55952380953], [1.63607694E12, 12504.611764705885], [1.63607676E12, 12366.946428571424], [1.63607682E12, 12360.635294117646], [1.63607664E12, 11845.348571428574], [1.63607712E12, 12568.264705882346], [1.6360767E12, 11921.23204419889], [1.63607718E12, 12910.023809523811], [1.636077E12, 12380.751479289946]], "isOverall": false, "label": "HTTP\u8BF7\u6C42", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.63607718E12, "title": "Latencies Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average response latencies in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendLatenciesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average latency was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesLatenciesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotLatenciesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewLatenciesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Latencies Over Time
function refreshLatenciesOverTime(fixTimestamps) {
    var infos = latenciesOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyLatenciesOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotLatenciesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesLatenciesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotLatenciesOverTime", "#overviewLatenciesOverTime");
        $('#footerLatenciesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var connectTimeOverTimeInfos = {
        data: {"result": {"minY": 6.499999999999998, "minX": 1.63607658E12, "maxY": 13.664670658682622, "series": [{"data": [[1.63607658E12, 13.664670658682622], [1.63607706E12, 6.8095238095238075], [1.63607688E12, 9.583333333333334], [1.63607694E12, 6.499999999999998], [1.63607676E12, 7.095238095238096], [1.63607682E12, 7.729411764705881], [1.63607664E12, 7.188571428571432], [1.63607712E12, 8.741176470588238], [1.6360767E12, 7.13259668508287], [1.63607718E12, 6.523809523809524], [1.636077E12, 6.745562130177513]], "isOverall": false, "label": "HTTP\u8BF7\u6C42", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.63607718E12, "title": "Connect Time Over Time"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getConnectTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Average Connect Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendConnectTimeOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Average connect time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesConnectTimeOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotConnectTimeOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewConnectTimeOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Connect Time Over Time
function refreshConnectTimeOverTime(fixTimestamps) {
    var infos = connectTimeOverTimeInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyConnectTimeOverTime");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotConnectTimeOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesConnectTimeOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotConnectTimeOverTime", "#overviewConnectTimeOverTime");
        $('#footerConnectTimeOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var responseTimePercentilesOverTimeInfos = {
        data: {"result": {"minY": 3205.0, "minX": 1.63607658E12, "maxY": 24085.0, "series": [{"data": [[1.63607658E12, 18112.0], [1.63607706E12, 17507.0], [1.63607688E12, 15214.0], [1.63607694E12, 17033.0], [1.63607676E12, 19812.0], [1.63607682E12, 18313.0], [1.63607664E12, 20206.0], [1.63607712E12, 24085.0], [1.6360767E12, 22658.0], [1.63607718E12, 17507.0], [1.636077E12, 20711.0]], "isOverall": false, "label": "Max", "isController": false}, {"data": [[1.63607658E12, 3256.0], [1.63607706E12, 7805.0], [1.63607688E12, 9381.0], [1.63607694E12, 8220.0], [1.63607676E12, 8421.0], [1.63607682E12, 9825.0], [1.63607664E12, 3205.0], [1.63607712E12, 9058.0], [1.6360767E12, 3258.0], [1.63607718E12, 11229.0], [1.636077E12, 9176.0]], "isOverall": false, "label": "Min", "isController": false}, {"data": [[1.63607658E12, 14926.000000000004], [1.63607706E12, 14066.3], [1.63607688E12, 13902.3], [1.63607694E12, 14522.0], [1.63607676E12, 14254.4], [1.63607682E12, 14061.5], [1.63607664E12, 16796.2], [1.63607712E12, 14545.5], [1.6360767E12, 15776.0], [1.63607718E12, 14496.900000000001], [1.636077E12, 13809.0]], "isOverall": false, "label": "90th percentile", "isController": false}, {"data": [[1.63607658E12, 18072.56], [1.63607706E12, 17307.59], [1.63607688E12, 14984.92], [1.63607694E12, 16343.589999999993], [1.63607676E12, 18013.170000000006], [1.63607682E12, 16385.349999999977], [1.63607664E12, 19481.72000000001], [1.63607712E12, 24082.87], [1.6360767E12, 20762.160000000014], [1.63607718E12, 17507.0], [1.636077E12, 19751.300000000014]], "isOverall": false, "label": "99th percentile", "isController": false}, {"data": [[1.63607658E12, 16458.799999999996], [1.63607706E12, 14899.65], [1.63607688E12, 14350.149999999998], [1.63607694E12, 15173.699999999997], [1.63607676E12, 14721.15], [1.63607682E12, 14628.8], [1.63607664E12, 17460.199999999997], [1.63607712E12, 15533.899999999998], [1.6360767E12, 18771.100000000006], [1.63607718E12, 16810.65], [1.636077E12, 14714.0]], "isOverall": false, "label": "95th percentile", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.63607718E12, "title": "Response Time Percentiles Over Time (successful requests only)"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Response Time in ms",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: '#legendResponseTimePercentilesOverTime'
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s : at %x Response time was %y ms"
                }
            };
        },
        createGraph: function () {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesResponseTimePercentilesOverTime"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotResponseTimePercentilesOverTime"), dataset, options);
            // setup overview
            $.plot($("#overviewResponseTimePercentilesOverTime"), dataset, prepareOverviewOptions(options));
        }
};

// Response Time Percentiles Over Time
function refreshResponseTimePercentilesOverTime(fixTimestamps) {
    var infos = responseTimePercentilesOverTimeInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotResponseTimePercentilesOverTime"))) {
        infos.createGraph();
    }else {
        var choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimePercentilesOverTime", "#overviewResponseTimePercentilesOverTime");
        $('#footerResponseTimePercentilesOverTime .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var responseTimeVsRequestInfos = {
    data: {"result": {"minY": 12055.5, "minX": 1.0, "maxY": 12562.0, "series": [{"data": [[4.0, 12281.5], [2.0, 12062.5], [1.0, 12527.0], [5.0, 12529.0], [3.0, 12055.5], [6.0, 12562.0], [7.0, 12242.0]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 7.0, "title": "Response Time Vs Request"}},
    getOptions: function() {
        return {
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Response Time in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: {
                noColumns: 2,
                show: true,
                container: '#legendResponseTimeVsRequest'
            },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median response time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesResponseTimeVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotResponseTimeVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewResponseTimeVsRequest"), dataset, prepareOverviewOptions(options));

    }
};

// Response Time vs Request
function refreshResponseTimeVsRequest() {
    var infos = responseTimeVsRequestInfos;
    prepareSeries(infos.data);
    if (isGraph($("#flotResponseTimeVsRequest"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesResponseTimeVsRequest");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotResponseTimeVsRequest", "#overviewResponseTimeVsRequest");
        $('#footerResponseRimeVsRequest .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};


var latenciesVsRequestInfos = {
    data: {"result": {"minY": 12050.0, "minX": 1.0, "maxY": 12555.5, "series": [{"data": [[4.0, 12265.0], [2.0, 12056.5], [1.0, 12516.5], [5.0, 12523.0], [3.0, 12050.0], [6.0, 12555.5], [7.0, 12235.0]], "isOverall": false, "label": "Successes", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 1000, "maxX": 7.0, "title": "Latencies Vs Request"}},
    getOptions: function() {
        return{
            series: {
                lines: {
                    show: false
                },
                points: {
                    show: true
                }
            },
            xaxis: {
                axisLabel: "Global number of requests per second",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            yaxis: {
                axisLabel: "Median Latency in ms",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 12,
                axisLabelFontFamily: 'Verdana, Arial',
                axisLabelPadding: 20,
            },
            legend: { noColumns: 2,show: true, container: '#legendLatencyVsRequest' },
            selection: {
                mode: 'xy'
            },
            grid: {
                hoverable: true // IMPORTANT! this is needed for tooltip to work
            },
            tooltip: true,
            tooltipOpts: {
                content: "%s : Median Latency time at %x req/s was %y ms"
            },
            colors: ["#9ACD32", "#FF6347"]
        };
    },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesLatencyVsRequest"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotLatenciesVsRequest"), dataset, options);
        // setup overview
        $.plot($("#overviewLatenciesVsRequest"), dataset, prepareOverviewOptions(options));
    }
};

// Latencies vs Request
function refreshLatenciesVsRequest() {
        var infos = latenciesVsRequestInfos;
        prepareSeries(infos.data);
        if(isGraph($("#flotLatenciesVsRequest"))){
            infos.createGraph();
        }else{
            var choiceContainer = $("#choicesLatencyVsRequest");
            createLegend(choiceContainer, infos);
            infos.createGraph();
            setGraphZoomable("#flotLatenciesVsRequest", "#overviewLatenciesVsRequest");
            $('#footerLatenciesVsRequest .legendColorBox > div').each(function(i){
                $(this).clone().prependTo(choiceContainer.find("li").eq(i));
            });
        }
};

var hitsPerSecondInfos = {
        data: {"result": {"minY": 0.11666666666666667, "minX": 1.63607658E12, "maxY": 3.3666666666666667, "series": [{"data": [[1.63607658E12, 3.3666666666666667], [1.63607706E12, 2.8], [1.63607688E12, 2.8], [1.63607694E12, 2.8333333333333335], [1.63607676E12, 2.8], [1.63607682E12, 2.8333333333333335], [1.63607664E12, 2.9166666666666665], [1.63607712E12, 2.8333333333333335], [1.6360767E12, 3.0166666666666666], [1.63607718E12, 0.11666666666666667], [1.636077E12, 2.816666666666667]], "isOverall": false, "label": "hitsPerSecond", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.63607718E12, "title": "Hits Per Second"}},
        getOptions: function() {
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of hits / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendHitsPerSecond"
                },
                selection: {
                    mode : 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y.2 hits/sec"
                }
            };
        },
        createGraph: function createGraph() {
            var data = this.data;
            var dataset = prepareData(data.result.series, $("#choicesHitsPerSecond"));
            var options = this.getOptions();
            prepareOptions(options, data);
            $.plot($("#flotHitsPerSecond"), dataset, options);
            // setup overview
            $.plot($("#overviewHitsPerSecond"), dataset, prepareOverviewOptions(options));
        }
};

// Hits per second
function refreshHitsPerSecond(fixTimestamps) {
    var infos = hitsPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if (isGraph($("#flotHitsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesHitsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotHitsPerSecond", "#overviewHitsPerSecond");
        $('#footerHitsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
}

var codesPerSecondInfos = {
        data: {"result": {"minY": 0.7, "minX": 1.63607658E12, "maxY": 3.0166666666666666, "series": [{"data": [[1.63607658E12, 2.783333333333333], [1.63607706E12, 2.8], [1.63607688E12, 2.8], [1.63607694E12, 2.8333333333333335], [1.63607676E12, 2.8], [1.63607682E12, 2.8333333333333335], [1.63607664E12, 2.9166666666666665], [1.63607712E12, 2.8333333333333335], [1.6360767E12, 3.0166666666666666], [1.63607718E12, 0.7], [1.636077E12, 2.816666666666667]], "isOverall": false, "label": "200", "isController": false}], "supportsControllersDiscrimination": false, "granularity": 60000, "maxX": 1.63607718E12, "title": "Codes Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of responses / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendCodesPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "Number of Response Codes %s at %x was %y.2 responses / sec"
                }
            };
        },
    createGraph: function() {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesCodesPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotCodesPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewCodesPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Codes per second
function refreshCodesPerSecond(fixTimestamps) {
    var infos = codesPerSecondInfos;
    prepareSeries(infos.data);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotCodesPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesCodesPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotCodesPerSecond", "#overviewCodesPerSecond");
        $('#footerCodesPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var transactionsPerSecondInfos = {
        data: {"result": {"minY": 0.7, "minX": 1.63607658E12, "maxY": 3.0166666666666666, "series": [{"data": [[1.63607658E12, 2.783333333333333], [1.63607706E12, 2.8], [1.63607688E12, 2.8], [1.63607694E12, 2.8333333333333335], [1.63607676E12, 2.8], [1.63607682E12, 2.8333333333333335], [1.63607664E12, 2.9166666666666665], [1.63607712E12, 2.8333333333333335], [1.6360767E12, 3.0166666666666666], [1.63607718E12, 0.7], [1.636077E12, 2.816666666666667]], "isOverall": false, "label": "HTTP\u8BF7\u6C42-success", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.63607718E12, "title": "Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTransactionsPerSecond"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                }
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTransactionsPerSecond"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTransactionsPerSecond"), dataset, options);
        // setup overview
        $.plot($("#overviewTransactionsPerSecond"), dataset, prepareOverviewOptions(options));
    }
};

// Transactions per second
function refreshTransactionsPerSecond(fixTimestamps) {
    var infos = transactionsPerSecondInfos;
    prepareSeries(infos.data);
    if(infos.data.result.series.length == 0) {
        setEmptyGraph("#bodyTransactionsPerSecond");
        return;
    }
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotTransactionsPerSecond"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTransactionsPerSecond");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTransactionsPerSecond", "#overviewTransactionsPerSecond");
        $('#footerTransactionsPerSecond .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

var totalTPSInfos = {
        data: {"result": {"minY": 0.7, "minX": 1.63607658E12, "maxY": 3.0166666666666666, "series": [{"data": [[1.63607658E12, 2.783333333333333], [1.63607706E12, 2.8], [1.63607688E12, 2.8], [1.63607694E12, 2.8333333333333335], [1.63607676E12, 2.8], [1.63607682E12, 2.8333333333333335], [1.63607664E12, 2.9166666666666665], [1.63607712E12, 2.8333333333333335], [1.6360767E12, 3.0166666666666666], [1.63607718E12, 0.7], [1.636077E12, 2.816666666666667]], "isOverall": false, "label": "Transaction-success", "isController": false}, {"data": [], "isOverall": false, "label": "Transaction-failure", "isController": false}], "supportsControllersDiscrimination": true, "granularity": 60000, "maxX": 1.63607718E12, "title": "Total Transactions Per Second"}},
        getOptions: function(){
            return {
                series: {
                    lines: {
                        show: true
                    },
                    points: {
                        show: true
                    }
                },
                xaxis: {
                    mode: "time",
                    timeformat: getTimeFormat(this.data.result.granularity),
                    axisLabel: getElapsedTimeLabel(this.data.result.granularity),
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20,
                },
                yaxis: {
                    axisLabel: "Number of transactions / sec",
                    axisLabelUseCanvas: true,
                    axisLabelFontSizePixels: 12,
                    axisLabelFontFamily: 'Verdana, Arial',
                    axisLabelPadding: 20
                },
                legend: {
                    noColumns: 2,
                    show: true,
                    container: "#legendTotalTPS"
                },
                selection: {
                    mode: 'xy'
                },
                grid: {
                    hoverable: true // IMPORTANT! this is needed for tooltip to
                                    // work
                },
                tooltip: true,
                tooltipOpts: {
                    content: "%s at %x was %y transactions / sec"
                },
                colors: ["#9ACD32", "#FF6347"]
            };
        },
    createGraph: function () {
        var data = this.data;
        var dataset = prepareData(data.result.series, $("#choicesTotalTPS"));
        var options = this.getOptions();
        prepareOptions(options, data);
        $.plot($("#flotTotalTPS"), dataset, options);
        // setup overview
        $.plot($("#overviewTotalTPS"), dataset, prepareOverviewOptions(options));
    }
};

// Total Transactions per second
function refreshTotalTPS(fixTimestamps) {
    var infos = totalTPSInfos;
    // We want to ignore seriesFilter
    prepareSeries(infos.data, false, true);
    if(fixTimestamps) {
        fixTimeStamps(infos.data.result.series, 28800000);
    }
    if(isGraph($("#flotTotalTPS"))){
        infos.createGraph();
    }else{
        var choiceContainer = $("#choicesTotalTPS");
        createLegend(choiceContainer, infos);
        infos.createGraph();
        setGraphZoomable("#flotTotalTPS", "#overviewTotalTPS");
        $('#footerTotalTPS .legendColorBox > div').each(function(i){
            $(this).clone().prependTo(choiceContainer.find("li").eq(i));
        });
    }
};

// Collapse the graph matching the specified DOM element depending the collapsed
// status
function collapse(elem, collapsed){
    if(collapsed){
        $(elem).parent().find(".fa-chevron-up").removeClass("fa-chevron-up").addClass("fa-chevron-down");
    } else {
        $(elem).parent().find(".fa-chevron-down").removeClass("fa-chevron-down").addClass("fa-chevron-up");
        if (elem.id == "bodyBytesThroughputOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshBytesThroughputOverTime(true);
            }
            document.location.href="#bytesThroughputOverTime";
        } else if (elem.id == "bodyLatenciesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesOverTime(true);
            }
            document.location.href="#latenciesOverTime";
        } else if (elem.id == "bodyCustomGraph") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCustomGraph(true);
            }
            document.location.href="#responseCustomGraph";
        } else if (elem.id == "bodyConnectTimeOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshConnectTimeOverTime(true);
            }
            document.location.href="#connectTimeOverTime";
        } else if (elem.id == "bodyResponseTimePercentilesOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimePercentilesOverTime(true);
            }
            document.location.href="#responseTimePercentilesOverTime";
        } else if (elem.id == "bodyResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeDistribution();
            }
            document.location.href="#responseTimeDistribution" ;
        } else if (elem.id == "bodySyntheticResponseTimeDistribution") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshSyntheticResponseTimeDistribution();
            }
            document.location.href="#syntheticResponseTimeDistribution" ;
        } else if (elem.id == "bodyActiveThreadsOverTime") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshActiveThreadsOverTime(true);
            }
            document.location.href="#activeThreadsOverTime";
        } else if (elem.id == "bodyTimeVsThreads") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTimeVsThreads();
            }
            document.location.href="#timeVsThreads" ;
        } else if (elem.id == "bodyCodesPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshCodesPerSecond(true);
            }
            document.location.href="#codesPerSecond";
        } else if (elem.id == "bodyTransactionsPerSecond") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTransactionsPerSecond(true);
            }
            document.location.href="#transactionsPerSecond";
        } else if (elem.id == "bodyTotalTPS") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshTotalTPS(true);
            }
            document.location.href="#totalTPS";
        } else if (elem.id == "bodyResponseTimeVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshResponseTimeVsRequest();
            }
            document.location.href="#responseTimeVsRequest";
        } else if (elem.id == "bodyLatenciesVsRequest") {
            if (isGraph($(elem).find('.flot-chart-content')) == false) {
                refreshLatenciesVsRequest();
            }
            document.location.href="#latencyVsRequest";
        }
    }
}

/*
 * Activates or deactivates all series of the specified graph (represented by id parameter)
 * depending on checked argument.
 */
function toggleAll(id, checked){
    var placeholder = document.getElementById(id);

    var cases = $(placeholder).find(':checkbox');
    cases.prop('checked', checked);
    $(cases).parent().children().children().toggleClass("legend-disabled", !checked);

    var choiceContainer;
    if ( id == "choicesBytesThroughputOverTime"){
        choiceContainer = $("#choicesBytesThroughputOverTime");
        refreshBytesThroughputOverTime(false);
    } else if(id == "choicesResponseTimesOverTime"){
        choiceContainer = $("#choicesResponseTimesOverTime");
        refreshResponseTimeOverTime(false);
    }else if(id == "choicesResponseCustomGraph"){
        choiceContainer = $("#choicesResponseCustomGraph");
        refreshCustomGraph(false);
    } else if ( id == "choicesLatenciesOverTime"){
        choiceContainer = $("#choicesLatenciesOverTime");
        refreshLatenciesOverTime(false);
    } else if ( id == "choicesConnectTimeOverTime"){
        choiceContainer = $("#choicesConnectTimeOverTime");
        refreshConnectTimeOverTime(false);
    } else if ( id == "choicesResponseTimePercentilesOverTime"){
        choiceContainer = $("#choicesResponseTimePercentilesOverTime");
        refreshResponseTimePercentilesOverTime(false);
    } else if ( id == "choicesResponseTimePercentiles"){
        choiceContainer = $("#choicesResponseTimePercentiles");
        refreshResponseTimePercentiles();
    } else if(id == "choicesActiveThreadsOverTime"){
        choiceContainer = $("#choicesActiveThreadsOverTime");
        refreshActiveThreadsOverTime(false);
    } else if ( id == "choicesTimeVsThreads"){
        choiceContainer = $("#choicesTimeVsThreads");
        refreshTimeVsThreads();
    } else if ( id == "choicesSyntheticResponseTimeDistribution"){
        choiceContainer = $("#choicesSyntheticResponseTimeDistribution");
        refreshSyntheticResponseTimeDistribution();
    } else if ( id == "choicesResponseTimeDistribution"){
        choiceContainer = $("#choicesResponseTimeDistribution");
        refreshResponseTimeDistribution();
    } else if ( id == "choicesHitsPerSecond"){
        choiceContainer = $("#choicesHitsPerSecond");
        refreshHitsPerSecond(false);
    } else if(id == "choicesCodesPerSecond"){
        choiceContainer = $("#choicesCodesPerSecond");
        refreshCodesPerSecond(false);
    } else if ( id == "choicesTransactionsPerSecond"){
        choiceContainer = $("#choicesTransactionsPerSecond");
        refreshTransactionsPerSecond(false);
    } else if ( id == "choicesTotalTPS"){
        choiceContainer = $("#choicesTotalTPS");
        refreshTotalTPS(false);
    } else if ( id == "choicesResponseTimeVsRequest"){
        choiceContainer = $("#choicesResponseTimeVsRequest");
        refreshResponseTimeVsRequest();
    } else if ( id == "choicesLatencyVsRequest"){
        choiceContainer = $("#choicesLatencyVsRequest");
        refreshLatenciesVsRequest();
    }
    var color = checked ? "black" : "#818181";
    if(choiceContainer != null) {
        choiceContainer.find("label").each(function(){
            this.style.color = color;
        });
    }
}

