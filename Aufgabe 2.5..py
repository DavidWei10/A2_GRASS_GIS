#!/usr/bin/env python3

import grass.script as gscript


def main():
    gscript.run_command('g.region', vector="motorways", overwrite=True)



    gscript.run_command('v.buffer',input="motorways",

    output="motorways_buffered", type="line", distance="1000", overwrite=True)



    gscript.run_command('v.to.rast', input="motorways_buffered",

    output="motorways_buffered_raster", use="cat", overwrite=True)

    

    gscript.run_command('v.db.addtable', map="motorways_buffered" , overwrite=True)

    

    gscript.run_command('r.stats.zonal', base="motorways_buffered_raster", 

    cover="GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3",

    method="sum" ,output="motorways_population", overwrite=True)

    

    distances=[250,500,1000,2500,5000]
    count=1
    

    for distance in distances:
        print(distance)

        gscript.run_command('g.region', vector="motorways" , overwrite=True)



        gscript.run_command('v.buffer', input="motorways",

        output="motorways_buffered" +str(count), type="line", distance=distances, overwrite=True)



        gscript.run_command('v.to.rast', input="motorways_buffered" +str(count),

        output="motorways_buffered_raster" +str(count), use="cat", overwrite=True)

    

        gscript.run_command('v.db.addtable',map="motorways_buffered" +str(count), overwrite=True) 

        

        gscript.run_command('r.stats.zonal', base="motorways_buffered_raster" +str(count), 

        cover="GHS_POP_E2015_GLOBE_R2019A_54009_250_V1_0_18_3", 

        method="sum" ,output="motorways_population" +str(count),overwrite=True)

        count=count +1

if __name__ == '__main__':
    main()
