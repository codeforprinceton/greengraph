class AddBillDateToUserSubmitted < ActiveRecord::Migration
  def change
    add_column :user_submitteds, :bill_date, :datetime
  end
end
