class CreateReadings < ActiveRecord::Migration
  def change
    create_table :readings do |t|
      t.timestamp :read_date
      t.text :city_code
      t.text :business_class
      t.decimal :gas_billed
      t.integer :gas_customer
      t.decimal :electric_billed
      t.integer :electric_customer

      t.timestamps null: false
    end
  end
end
