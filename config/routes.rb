Rails.application.routes.draw do
  root 'home#index'
  match 'about', to: 'home#about', via: 'get', as: 'about'
  match 'start', to: 'home#getstarted', via: 'get', as: 'start'
  match 'analytics', to: 'analytics#index', via: 'get', as: 'analytics'
  match 'analytics/search', to: 'analytics#search', via: 'get', as: 'search'
  match 'analytics/range', to: 'analytics#daterangechart', via: 'post', as: 'daterangechart_path'
  match 'api', to: 'api#index', via: 'get', as: 'api'
  match 'api/raw', to: 'api#raw', via: 'get', as: 'raw_api'
  match 'api/rawtemp', to: 'api#rawtemp', via: 'get', as: 'raw_api_temp'
  match 'api/geojson', to: 'api#geojson', via: 'get', as: 'raw_api_geojson'
  match 'api/models', to: 'api#models', via: 'get', as: 'raw_api_models'
  match 'maps', to: 'maps#index', via: 'get', as: 'maps'
  match 'dashboard', to: 'dashboard#index', via: 'get', as: 'dashboard'
  match 'dashboard/history', to: 'dashboard#history', via: 'get', as: 'dashboard_history'
  match 'dashboard/add', to: 'dashboard#add', via: 'get', as: 'dashboard_add'
  match 'dashboard/update', to: 'dashboard#update', via: 'post', as: 'dashboard_update'
  match 'dashboard/:id/delete', to: 'dashboard#delete', via: 'delete', as: 'dashboard_delete'
  match 'dashboard/:id', to: 'dashboard#show', via: 'get', as: 'dashboard_item'
  devise_for :users, controllers: { sessions: "users/sessions", registrations: "users/registrations"}
  match 'import', to: 'import#index', via: 'get', as: 'import'
  match 'import/submitfile', to: 'import#submitfile', via: 'post', as: 'submitfile'

end
