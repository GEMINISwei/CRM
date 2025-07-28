let db = db.getSiblingDB('crm')

db.createCollection('user')
db.user.createIndex({ 'username': 1 }, { unique: true })
db.user.insertMany([
  {
    username: 'wei',
    password: '$2b$12$/6opSuO0VeHkunzJbzLCfuuoKwsqHL2RYCuOlfpUootztwVgKe28G',
    disabled: false,
    access_token: '',
    shift: 'admin',
    level_group: 'Initialize'
  },
  {
    username: 'gogo5757',
    password: '$2b$12$rXoKzVkDzYibIaPg8Spz0Ol1IAGk1SHJD0dA9WWB7hkAD.bruKbdO',
    disabled: false,
    access_token: '',
    shift: 'admin',
    level_group: 'Initialize'
  }
])

db.createCollection('game')
db.game.createIndex({ 'name': 1 }, { unique: true })

db.createCollection('member')

db.createCollection('player')

db.createCollection('property')

db.createCollection('stock')

db.createCollection('trade')

db.createCollection('activity')

db.createCollection('setting')
db.setting.insertMany([
  {
    collection_name: 'member',
    fields: {
      communication_way: []
    }
  },
  {
    collection_name: 'trade',
    fields: {
      supermarket_stage_fee: 5,
      v_account_stage_fee: -10,
      color: {
        admin: '#ffffff',
        day_class: '#e0ffcf',
        night_class: '#fff6cf'
      }
    }
  },
  {
    collection_name: 'award',
    fields: {
      block: {
        one_award: 1,
        two_award: 1,
        three_award: 2,
        no_award: 8
      }
    }
  }
])
