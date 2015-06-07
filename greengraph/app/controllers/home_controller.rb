class HomeController < ApplicationController
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
            @commercialgas = Reading.billsum("gas", comgasboro, comgastwp) + Reading.billsum("gas", indgasboro, indgastwp)
      @residentialgas = Reading.billsum("gas", resgasboro, resgastwp)
      @commercialelectric = Reading.billsum("electric", comelectricboro, comelectrictwp) + Reading.billsum("electric", indelectricboro, indelectrictwp)
      @residentialelectric = Reading.billsum("electric", reselectricboro, reselectrictwp)
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
  end
  
  def about
  end
end
