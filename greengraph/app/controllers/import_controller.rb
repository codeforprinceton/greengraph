class ImportController < ApplicationController
  def index
  end

  def submitfile
    Import.parsefile(params[:file][:uploaded_file].tempfile)
  end
end
