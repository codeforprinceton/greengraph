class ImportController < ApplicationController
  before_action :authenticate_user!
  
  def index
  end

  def submitfile
    Import.parsefile(params[:file][:uploaded_file].tempfile)
  end
end
