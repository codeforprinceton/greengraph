class AddReadingToUserSubmitted < ActiveRecord::Migration
  def change
    add_column :user_submitteds, :gas_reading, :integer
    add_column :user_submitteds, :electric_reading, :integer
    add_column :user_submitteds, :electric_charge, :float
    add_column :user_submitteds, :gas_charge, :float
  end
end
