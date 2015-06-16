class RemoveGasReadingFromUserSubmitted < ActiveRecord::Migration
  def change
    remove_column :user_submitteds, :gas_reading, :integer
  end
end
