let db = db.getSiblingDB('crm')

db.createCollection('user')
db.user.createIndex({ 'username': 1 }, { unique: true })
db.user.insertMany([
  {
    nickname: '小威',
    username: 'wei',
    password: '$2b$12$/6opSuO0VeHkunzJbzLCfuuoKwsqHL2RYCuOlfpUootztwVgKe28G',
    shift: 'admin',
    disabled: false,
    access_token: '',
    level_group: 'Admin'
  },
  {
    nickname: 'GoGo Test',
    username: 'gogo5757',
    password: '$2b$12$rXoKzVkDzYibIaPg8Spz0Ol1IAGk1SHJD0dA9WWB7hkAD.bruKbdO',
    shift: 'admin',
    disabled: false,
    access_token: '',
    level_group: 'Admin'
  }
])

db.createCollection('login_record')

db.createCollection('game')
db.game.createIndex({ 'name': 1 }, { unique: true })

db.createCollection('member')

db.createCollection('player')

db.createCollection('property')

db.createCollection('stock')

db.createCollection('trade')

db.createCollection('activity')

db.createCollection('lottery')

db.createCollection('setting')
db.setting.insertMany([
  {
    collection_name: 'permission',
    fields: {}
  },
  {
    collection_name: 'member',
    fields: {
      communication_way: []
    }
  },
  {
    collection_name: 'trade',
    fields: {
      fee: {
        supermarket_stage: 0,
        v_account_stage: 0,
      },
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
