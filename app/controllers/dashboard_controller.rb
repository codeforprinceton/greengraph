class DashboardController < ApplicationController
  before_action :authenticate_user!
  def index
    @found = current_user.UserSubmitted
    @gasusage = @found.where("gas_reading IS NOT NULL").pluck(:gas_reading)
    @gaslabels = @found.where("gas_reading IS NOT NULL").pluck(:created_at)
  end

  def show
  end
  
  def history
    @found = current_user.UserSubmitted
  end
  
  def add
    @submitted = UserSubmitted.new
  end
  
  def update
    @submitted = UserSubmitted.new(user_submitted_params)
    @submitted[:user_id] = current_user.id
    if @submitted.save
      flash[:notice] = "Saved successfully"
      return redirect_to dashboard_path
    else
      flash[:alert] = "Error saving"
      return render :update
    end
  end
  
  private
  
  def user_submitted_params
    params.require(:user_submitted).permit(:user_id, :electric_reading, :electric_charge, :gas_reading, :gas_charge)
  end
end
