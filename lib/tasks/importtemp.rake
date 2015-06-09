require 'csv'

namespace :csv do

  desc "Import Temperature CSV Data"
  task :importtemp => :environment do
    progressbar = ProgressBar.create(:title => 'Temperature CSV file import', :total => 408)
    csv_file_path = 'db/seeds/Temprature.csv'
    puts "Starting data import -- please wait"
    CSV.foreach(csv_file_path) do |row|
        (1..12).each do |x|
        Temperature.create!({
          :date => ("#{x.to_s}/01/#{row[0].to_s}").to_datetime, #grab the year from row 0, and add the # for the month
          :temp => row[x] #grab the corresponding temp from the correct colunm for each month
        })
        progressbar.increment
        end
    end
  end
end