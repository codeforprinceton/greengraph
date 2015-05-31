Rails.application.routes.draw do
  root 'home#index'
  match 'about', to: 'home#about', via: 'get', as: 'about'
  match 'analytics', to: 'analytics#index', via: 'get', as: 'analytics'
  match 'analytics/search', to: 'analytics#search', via: 'get', as: 'search'
  match 'analytics/range', to: 'analytics#daterangechart', via: 'post', as: 'daterangechart_path'
  match 'api', to: 'api#index', via: 'get', as: 'api'
  match 'api/raw', to: 'api#raw', via: 'get', as: 'raw_api'
end
