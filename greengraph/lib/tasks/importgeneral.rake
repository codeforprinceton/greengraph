require 'csv'

namespace :csv do

  desc "Import Generalized CSV Data"
  task :importgeneral => :environment do
    progressbar = ProgressBar.create(:title => 'General energy CSV file import', :total => 60)
    csv_file_path = 'db/seeds/princeton_energy_electrical.csv'
    puts "Starting data import -- please wait"
    CSV.foreach(csv_file_path) do |row|
        Generalenergy.create!({
          :date => if row[0] then row[0].to_datetime else row[0] end, #grab the year from row 0, and add the # for the month
          :usage => row[1] #grab the corresponding temp from the correct colunm for each month
        })
        progressbar.increment
    end
  end
end