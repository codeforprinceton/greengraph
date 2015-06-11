class Users::SessionsController < Devise::SessionsController
# before_filter :configure_sign_in_params, only: [:create]

  # GET /resource/sign_in
   def new
     super
   end

  # POST /resource/sign_in
   def create
     super
   end

  # DELETE /resource/sign_out
  # def destroy
  #   super
  # end

   protected

  # The path used after sign up.
  def after_sign_in_path_for(resource)
    flash[:notice] = "Welcome Back!"
    dashboard_path
  end
  
  def after_sign_out_path_for(resource)
    flash[:notice] = "Signed out successfully"
    root_path
  end

  # You can put the params you want to permit in the empty array.
  # def configure_sign_in_params
  #   devise_parameter_sanitizer.for(:sign_in) << :attribute
  # end
end
