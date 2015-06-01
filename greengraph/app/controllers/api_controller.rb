class ApiController < ApplicationController
  def index
  end
  
  def raw
      @alldata = Reading.all
      return render :json => @alldata.to_json
  end
  
  def rawtemp
      @alldata = Temperature.all.only(:date, :temp)
      return render :json => @alldata.to_json(:except => [:created_at, :updated_at, :id])
  end
end
