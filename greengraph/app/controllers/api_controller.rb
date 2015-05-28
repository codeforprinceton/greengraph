class ApiController < ApplicationController
  def index
  end
  
  def raw
      @alldata = Reading.all
      return render :json => @alldata.to_json
  end
end
