class AnalyticsController < ApplicationController
  def index
      #get all gas readings for each class
      comgasboro = Reading.getbill("gas", "Commercial", "PRINCETON BORO")
      comgastwp = Reading.getbill("gas", "Commercial", "PRINCETON TWP")
      indgasboro = Reading.getbill("gas", "Industrial", "PRINCETON BORO")
      indgastwp = Reading.getbill("gas", "Industrial", "PRINCETON TWP")
      resgasboro = Reading.getbill("gas", "Residential", "PRINCETON BORO")
      resgastwp = Reading.getbill("gas", "Residential", "PRINCETON TWP")
      @commercialgas = Reading.billsum("gas", comgasboro, comgastwp)
      @industrialgas = Reading.billsum("gas", indgasboro, indgastwp)
      @residentialgas = Reading.billsum("gas", resgasboro, resgastwp)
      #break down gas readings per reading per class -- MOVE THESE TO MODEL
      comgas2009 = comgasboro.where(read_date: DateTime.new(2009)..(DateTime.new(2010) - 1.month))
      indgas2009 = indgasboro.where(read_date: DateTime.new(2009)..(DateTime.new(2010) - 1.month))
      resgas2009 = resgasboro.where(read_date: DateTime.new(2009)..(DateTime.new(2010) - 1.month))
      @commercialgasbreakread = comgas2009.pluck(:read_date).map{|readdate| readdate.strftime("%B, %Y").gsub(/,/, '')}
      @commercialgasbreakbilled = comgas2009.pluck(:gas_billed)
      @industrialgasbreakread = indgas2009.pluck(:read_date).map{|readdate| readdate.strftime("%B, %Y").gsub(/,/, '')}
      @industrialgasbreakbilled = indgas2009.pluck(:gas_billed)
      @residentialgasbreakread = resgas2009.pluck(:read_date).map{|readdate| readdate.strftime("%B, %Y").gsub(/,/, '')}
      @residentialgasbreakbilled = resgas2009.pluck(:gas_billed)
  end
end
