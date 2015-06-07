class CreateGeneralenergies < ActiveRecord::Migration
  def change
    create_table :generalenergies do |t|
      t.datetime :date
      t.decimal :usage

      t.timestamps null: false
    end
  end
end
