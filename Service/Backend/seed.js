let db = db.getSiblingDB('crm')

// Game Collection Seed
db.createCollection('games')
db.games.createIndex({ 'name': 1 }, { unique: true })

// Member Collection Seed
db.createCollection('members')

// Property Collection Seed
db.createCollection('properties')

// Stock Collection Seed
db.createCollection('stocks')

// Trade Collection Seed
db.createCollection('trades')

// Setting Collection Seed
db.createCollection('settings')
db.settings.insertMany([
  {
    'collection_name': 'members',
    'fields': {
      'communication_ways': []
    }
  },
  {
    'collection_name': 'trades',
    'fields': {
      'supermarket_stage_fee': 5,
      'v_account_stage_fee': -10,
    }
  },
  {
    'collection_name': 'settings',
    'fields': {
      'admin_color': '#ffffff',
      'day_class_color': '#e0ffcf',
      'night_class_color': '#fff6cf',
    }
  }
])
