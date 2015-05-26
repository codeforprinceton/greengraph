Rails.application.routes.draw do
  root 'home#index'
  match 'analytics', to: 'analytics#index', via: 'get', as: 'analytics'
  match 'api', to: 'api#index', via: 'get', as: 'api'
  match 'api/raw', to: 'api#raw', via: 'get', as: 'raw_api'
end
