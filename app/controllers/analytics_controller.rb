class AnalyticsController < ApplicationController
  def index
      #get all initial gas readings for each class
      comgasboro = Reading.getbill("gas", "Commercial", "PRINCETON BORO")
      comgastwp = Reading.getbill("gas", "Commercial", "PRINCETON TWP")
      indgasboro = Reading.getbill("gas", "Industrial", "PRINCETON BORO")
      indgastwp = Reading.getbill("gas", "Industrial", "PRINCETON TWP")
      resgasboro = Reading.getbill("gas", "Residential", "PRINCETON BORO")
      resgastwp = Reading.getbill("gas", "Residential", "PRINCETON TWP")
      comelectricboro = Reading.getbill("electric", "Commercial", "PRINCETON BORO")
      comelectrictwp = Reading.getbill("electric", "Commercial", "PRINCETON TWP")
      indelectricboro = Reading.getbill("electric", "Industrial", "PRINCETON BORO")
      indelectrictwp = Reading.getbill("electric", "Industrial", "PRINCETON TWP")
      reselectricboro = Reading.getbill("electric", "Residential", "PRINCETON BORO")
      reselectrictwp = Reading.getbill("electric", "Residential", "PRINCETON TWP")
      #sum them up for the totals graph
      @commercialgas = Reading.billsum("gas", comgasboro, comgastwp) + Reading.billsum("gas", indgasboro, indgastwp)
      @residentialgas = Reading.billsum("gas", resgasboro, resgastwp)
      @commercialelectric = Reading.billsum("electric", comelectricboro, comelectrictwp) + Reading.billsum("electric", indelectricboro, indelectrictwp)
      @residentialelectric = Reading.billsum("electric", reselectricboro, reselectrictwp)
      #break down gas readings per reading per year
      @commercialgasbreakread = Reading.yeardaterange(comgasboro, 2009, 2010)
      @commercialgasbreakbilled = Reading.yeardatarange(comgasboro, "gas", 2009, 2010)
      @industrialgasbreakread = Reading.yeardaterange(indgasboro, 2009, 2010)
      @industrialgasbreakbilled = Reading.yeardatarange(indgasboro, "gas", 2009, 2010)
      @residentialgasbreakread = Reading.yeardaterange(resgasboro, 2009, 2010)
      @residentialgasbreakbilled = Reading.yeardatarange(resgasboro, "gas", 2009, 2010)
      @commercialelectricbreakread = Reading.yeardaterange(comelectricboro, 2009, 2010)
      @commercialelectricbreakbilled = Reading.yeardatarange(comelectricboro, "electric", 2009, 2010)
      @industrialelectricbreakread = Reading.yeardaterange(indelectricboro, 2009, 2010)
      @industrialelectricbreakbilled = Reading.yeardatarange(indelectricboro, "electric", 2009, 2010)
      @residentialelectricbreakread = Reading.yeardaterange(reselectricboro, 2009, 2010)
      @residentialelectricbreakbilled = Reading.yeardatarange(reselectricboro, "electric", 2009, 2010)
      
      #combine gas and electric to one usage
      @totalenergy = Reading.thmtokwh(@commercialgas) + Reading.thmtokwh(@residentialgas) + @commercialelectric + @residentialelectric
      #convert from KWH to Kw by dividing average hours in a month
      #NOT USED @totalenergy = @totalenergy / 730.484
      
      #convert kwh to co2 in metric tons
      @totalco2 = @totalenergy / 1428
      #convert kwh to cars on road
      @totalcars = @totalenergy / 10000
      #convert kwh to miles/year per passenger car
      @totalmiles = @totalenergy * 1.6
      #average home energy use
      @totalhome = @totalenergy / 10000
      #acres of forest needed
      @totalacres = @totalenergy / 1666.6667
      #tree seedlings grown for 10 years needed
      @totalseedlings = @totalenergy / 55.5556
      
      #for date range dropdowns
      @daterange = Reading.pluck(:read_date).map!{|x| x.strftime("%Y").gsub(/,/, '')}.uniq
      #for location dropdowns
      @location = Reading.pluck(:city_code).uniq.map!{|x| ["Former " + x.titleize, x.titleize]}
      @location += ["All"]
      
      
      
      @bigchartlabels = Generalenergy.pluck(:date).map!{|x| x.strftime("%m, %Y")}
      
      @bigchartdata = Generalenergy.pluck(:usage)
      
  end
  
  def search
  end
  
  def daterangechart
    @date = daterange_params[:year].to_i
    @location = daterange_params[:location]
    @type = daterange_params[:type]
    @class = daterange_params[:business_class]
    @datehigh = @date + 1
    initaldata = Reading.getbill(@type, @class, @location)
    @dataread = Reading.yeardaterange(initaldata, @date, @datehigh)
    @databilled = Reading.yeardatarange(initaldata, @type, @date, @datehigh)
    @class = @class.downcase
    render partial: 'analytics/graphs/chartdata.js.erb'
  end
  
  private
  
  def daterange_params
    params.permit(:location, :type, :year, :business_class)
  end
end
