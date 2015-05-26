class AnalyticsController < ApplicationController
  def index
      #get all gas readings for each class
      @commercialgas = Reading.where('business_class = ? and gas_billed IS NOT NULL', "Commercial").pluck(:gas_billed).sum
      @industrialgas = Reading.where('business_class = ? and gas_billed IS NOT NULL', "Industrial").pluck(:gas_billed).sum
      @residentialgas = Reading.where('business_class = ? and gas_billed IS NOT NULL', "Residential").pluck(:gas_billed).sum
  end
end
