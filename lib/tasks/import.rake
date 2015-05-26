require 'csv'

namespace :csv do

  desc "Import CSV Data"
  task :import => :environment do
    progressbar = ProgressBar.create(:title => 'CSV file import', :total => 552)
    csv_file_path = 'db/seeds/DataImport.csv'
    puts "Starting data import -- please wait"
    CSV.foreach(csv_file_path) do |row|
      Reading.create!({
        :read_date => if row[0] then row[0].to_datetime else row[0] end,
        :city_code => row[1],
        :business_class => row[2],  
        :gas_billed => if row[3] then row[3][0...-4].gsub(/,/, '') else row[3] end,  
        :gas_customer => row[4],  
        :electric_billed => if row[5] then row[5][0...-4].gsub(/,/, '') else row[5] end,   
        :electric_customer => row[6],       
      })
      progressbar.increment
    end
  end
end