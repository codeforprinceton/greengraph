class AddGasReadingToUserSubmitted < ActiveRecord::Migration
  def change
    add_column :user_submitteds, :gas_reading, :float
  end
end
