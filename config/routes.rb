Rails.application.routes.draw do
  root 'home#index'
  match 'api', to: 'api#index', via: 'get', as: 'api'
  match 'analytics', to: 'analytics#index', via: 'get', as: 'analytics'
end
