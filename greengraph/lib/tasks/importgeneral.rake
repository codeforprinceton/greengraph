require 'csv'

namespace :csv do

  desc "Import Generalized CSV Data"
  task :importgeneral => :environment do
    progressbar = ProgressBar.create(:title => 'General energy CSV file import', :total => 60)
    csv_file_path = 'db/seeds/princeton_energy_electrical.csv'
    puts "Starting data import -- please wait"
    CSV.foreach(csv_file_path) do |row|
        Generalenergy.create!({
          :date => if row[0] then ("01/#{row[0][0..1].to_s}/#{row[0][3..-1].to_s}").to_datetime else row[0] end, 
          :usage => row[1]
        })
        progressbar.increment
    end
  end
end