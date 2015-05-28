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
  end
  
  def search
  end
end
