require 'csv'

namespace :csv do

  desc "Import Temperature CSV Data"
  task :import => :environment do
    progressbar = ProgressBar.create(:title => 'Temperature CSV file import', :total => 1452)
    csv_file_path = 'db/seeds/Temprature.csv'
    puts "Starting data import -- please wait"
    CSV.foreach(csv_file_path) do |row|
      Temperature.create!({
        :date => if row[0] then row[0].to_datetime else row[0] end,
        :temp => row[1]
      })
      progressbar.increment
    end
  end
end