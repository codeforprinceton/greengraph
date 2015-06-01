# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rake db:seed (or created alongside the db with db:setup).

unless Reading.last
    Rake::Task['csv:import'].invoke
end
unless Temperature.last
    Rake::Task['csv:importtemp'].invoke
end