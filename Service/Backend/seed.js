let db = db.getSiblingDB('crm')

db.createCollection('user')
db.user.createIndex({ 'username': 1 }, { unique: true })

db.createCollection('game')
db.game.createIndex({ 'name': 1 }, { unique: true })

db.createCollection('member')

db.createCollection('property')

db.createCollection('stock')

db.createCollection('trade')

db.createCollection('activity')

db.createCollection('setting')
db.setting.insertMany([
  {
    'collection_name': 'member',
    'fields': {
      'communication_way': []
    }
  },
  {
    'collection_name': 'trade',
    'fields': {
      'supermarket_stage_fee': 5,
      'v_account_stage_fee': -10,
    }
  },
  {
    'collection_name': 'system',
    'fields': {
      'admin_color': '#ffffff',
      'day_class_color': '#e0ffcf',
      'night_class_color': '#fff6cf',
    }
  }
])
