Rails.application.routes.draw do
  get 'dashboard/index'

  get 'dashboard/show'

  root 'home#index'
  match 'about', to: 'home#about', via: 'get', as: 'about'
  match 'analytics', to: 'analytics#index', via: 'get', as: 'analytics'
  match 'analytics/search', to: 'analytics#search', via: 'get', as: 'search'
  match 'analytics/range', to: 'analytics#daterangechart', via: 'post', as: 'daterangechart_path'
  match 'api', to: 'api#index', via: 'get', as: 'api'
  match 'api/raw', to: 'api#raw', via: 'get', as: 'raw_api'
  match 'api/rawtemp', to: 'api#rawtemp', via: 'get', as: 'raw_api_temp'
  match 'api/geojson', to: 'api#geojson', via: 'get', as: 'raw_api_geojson'
  match 'maps', to: 'maps#index', via: 'get', as: 'maps'
  match 'dashboard', to: 'dashboard#index', via: 'get', as: 'dashboard'
  match 'dashboard/:id', to: 'dashboard#show', via: 'get', as: 'dashboard_item'
  devise_for :users, controllers: { sessions: "users/sessions" }
  match 'import', to: 'import#index', via: 'get', as: 'import'
  match 'import/submitfile', to: 'import#submitfile', via: 'post', as: 'submitfile'

end
