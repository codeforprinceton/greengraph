class AnalyticsController < ApplicationController
  def index
      #get all initial gas readings for each class
      comgasboro = Reading.getbill("gas", "Commercial", "PRINCETON BORO")
      comgastwp = Reading.getbill("gas", "Commercial", "PRINCETON TWP")
      indgasboro = Reading.getbill("gas", "Industrial", "PRINCETON BORO")
      indgastwp = Reading.getbill("gas", "Industrial", "PRINCETON TWP")
      resgasboro = Reading.getbill("gas", "Residential", "PRINCETON BORO")
      resgastwp = Reading.getbill("gas", "Residential", "PRINCETON TWP")
      #sum them up for the totals graph
      @commercialgas = Reading.billsum("gas", comgasboro, comgastwp)
      @industrialgas = Reading.billsum("gas", indgasboro, indgastwp)
      @residentialgas = Reading.billsum("gas", resgasboro, resgastwp)
      #break down gas readings per reading per year
      @commercialgasbreakread = Reading.yeardaterange(comgasboro, 2009, 2010)
      @commercialgasbreakbilled = Reading.yeardatarange(comgasboro, "gas", 2009, 2010)
      @industrialgasbreakread = Reading.yeardaterange(indgasboro, 2009, 2010)
      @industrialgasbreakbilled = Reading.yeardatarange(indgasboro, "gas", 2009, 2010)
      @residentialgasbreakread = Reading.yeardaterange(resgasboro, 2009, 2010)
      @residentialgasbreakbilled = Reading.yeardatarange(resgasboro, "gas", 2009, 2010)
  end
end
