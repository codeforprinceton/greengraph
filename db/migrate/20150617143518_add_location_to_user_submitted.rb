class AddLocationToUserSubmitted < ActiveRecord::Migration
  def change
    add_column :user_submitteds, :city, :string
    add_column :user_submitteds, :state, :string
    add_column :user_submitteds, :zip, :string
  end
end
