class CreateTemperatures < ActiveRecord::Migration
  def change
    create_table :temperatures do |t|
      t.datetime :date
      t.decimal :temp

      t.timestamps null: false
    end
  end
end
