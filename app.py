from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Дані про напої та їх ціни
DRINKS_DATA = {
    'energy': {
        'budget': {'price': 30, 'brands': ['Non Stop', 'Pit Bull', 'Best Shot', 'Battery']},
        'medium': {'price': 50, 'brands': ['Hell', 'Burn', 'Battery (деякі лінійки)']},
        'premium': {'price': 70, 'brands': ['Red Bull', 'Monster Energy']}
    },
    'alcohol': {
        'budget': {'price': 35, 'brands': ['Shake', 'Revo', 'King\'s Bridge']},
        'medium': {'price': 55, 'brands': ['Garage', 'Somersby', 'Seth & Riley\'s Garage']},
        'premium': {'price': 100, 'brands': ['Strongbow', 'Magners', 'Rekorderlig']}
    },
    'coffee': {
        'budget': {'price': 40, 'brands': ['Кава з автомата', 'Магазинна розчинна']},
        'medium': {'price': 60, 'brands': ['Кав\'ярня середнього класу', 'McDonald\'s']},
        'premium': {'price': 90, 'brands': ['Starbucks', 'Львівська каварня']}
    },
    'soda': {
        'budget': {'price': 15, 'brands': ['Кола-пепсі дешеві аналоги']},
        'medium': {'price': 25, 'brands': ['Coca-Cola, Pepsi, Fanta']},
        'premium': {'price': 40, 'brands': ['Імпортні, крафтові лимонади']}
    }
}

# Дані про куріння
SMOKING_DATA = {
    'cigarettes': {
        'price_per_pack': 130,
        'cigarettes_per_pack': 20,
        'price_per_cigarette': 6.5
    },
    'vape': {
        'disposable': {'price': 300},
        'reusable': {'price': 800, 'monthly_maintenance': 900}
    },
    'hookah': {
        'price_per_session': 250,
        'coal_price': 50,
        'tobacco_price': 150
    },
    'chewing_tobacco': {
        'price_per_pack': 80,
        'packs_per_week': 3
    }
}

# Дані про фастфуд
JUNK_FOOD_DATA = {
    'chips': {
        'price_per_pack': 45,
        'brands': ['Pringles', 'Lays', 'Cheetos']
    },
    'pizza': {
        'budget': {'price': 120, 'brands': ['Піца швидкого приготування']},
        'medium': {'price': 200, 'brands': ['Domino\'s, Pizza Hut']},
        'premium': {'price': 350, 'brands': ['Ресторанна піца']}
    },
    'burgers': {
        'budget': {'price': 80, 'brands': ['МакАвто, локальні бургерні']},
        'medium': {'price': 150, 'brands': ['McDonald\'s, KFC']},
        'premium': {'price': 250, 'brands': ['Gastro Pub, крафтові бургери']}
    },
    'sweets': {
        'price_per_pack': 60,
        'brands': ['Шоколадки, цукерки, випічка']
    }
}

# Дані про азартні ігри
GAMBLING_DATA = {
    'lottery': {
        'price_per_ticket': 50,
        'tickets_per_week': 4
    },
    'casino': {
        'budget': {'daily_loss': 200},
        'medium': {'daily_loss': 500},
        'high': {'daily_loss': 1000}
    },
    'betting': {
        'budget': {'weekly_bet': 100},
        'medium': {'weekly_bet': 300},
        'high': {'weekly_bet': 700}
    }
}

# Можливі захворювання
DISEASES = {
    'energy': [
        'Прискорене серцебиття',
        'Підвищення артеріального тиску',
        'Безсоння',
        'Хронічна втома',
        'Дратівливість',
        'Порушення нервової системи',
        'Залежність від кофеїну',
        'Проблеми із серцево-судинною системою'
    ],
    'alcohol': [
        'Ураження печінки',
        'Проблеми із серцем',
        'Погіршення пам\'яті та уваги',
        'Алкогольна залежність',
        'Цироз печінки',
        'Проблеми із травною системою',
        'Психічні розлади',
        'Захворювання підшлункової залози'
    ],
    'smoking': [
        'Рак легенів',
        'Інфаркт міокарда',
        'Інсульт',
        'Артеріальна гіпертензія',
        'Стенокардія',
        'Ендартеріїт (ураження артерій нижніх кінцівок)',
        'Хронічний бронхіт',
        'Рак інших органів'
    ],
    'coffee': [
        'Безсоння',
        'Тривожність',
        'Проблеми із шлунком',
        'Порушення серцевого ритму',
        'Залежність від кофеїну',
        'Головний біль при відміні'
    ],
    'soda': [
        'Цукровий діабет 2 типу',
        'Ожиріння',
        'Проблеми із зубами',
        'Остеопороз',
        'Хвороби нирок'
    ],
    'junk_food': [
        'Ожиріння',
        'Цукровий діабет',
        'Хвороби серцево-судинної системи',
        'Високий холестерин',
        'Проблеми із травленням',
        'Акне та проблеми зі шкірою'
    ],
    'gambling': [
        'Лудоманія (ігрова залежність)',
        'Депресія',
        'Тривожні розлади',
        'Суїцидальні думки',
        'Фінансове банкрутство',
        'Проблеми у стосунках',
        'Втрата роботи',
        'Соціальна ізоляція'
    ]
}

# Ідеї для заощаджень
SAVING_IDEAS = [
    {'name': 'Новий смартфон', 'price': '8000-20000 грн'},
    {'name': 'Ноутбук', 'price': '15000-40000 грн'},
    {'name': 'Подорож до Європи', 'price': '20000-50000 грн'},
    {'name': 'Курси програмування', 'price': '5000-15000 грн'},
    {'name': 'Абонемент у спортзал', 'price': '800-2000 грн/рік'},
    {'name': 'Набір для хобі', 'price': '1000-5000 грн'},
    {'name': 'Інвестиції в криптовалюту', 'price': 'від 1000 грн'},
    {'name': 'Оренда квартири на місяць', 'price': '8000-15000 грн'},
    {'name': 'Новий велосипед', 'price': '5000-15000 грн'},
    {'name': 'Професійна камера', 'price': '10000-30000 грн'},
    {'name': 'Музичний інструмент', 'price': '3000-20000 грн'},
    {'name': 'Курси водіння', 'price': '4000-8000 грн'},
    {'name': 'Бізнес-ідея стартап', 'price': '10000-100000 грн'},
    {'name': 'Накопичення на авто', 'price': '50000-300000 грн'},
    {'name': 'Інвестиції в акції', 'price': 'від 1000 грн'},
    {'name': 'Курси іноземної мови', 'price': '3000-10000 грн'},
    {'name': 'Ремонт у квартирі', 'price': '10000-100000 грн'},
    {'name': 'Похід в гори', 'price': '2000-8000 грн'},
    {'name': 'Квитки на концерт улюбленого гурту', 'price': '500-3000 грн'},
    {'name': 'Новий гардероб', 'price': '3000-15000 грн'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    results = {
        'total_cost_year': 0,
        'total_cost_month': 0,
        'total_cost_week': 0,
        'total_cost_day': 0,
        'breakdown': [],
        'diseases': [],
        'saving_ideas': []
    }
    
    # Розрахунок енергетиків
    if data.get('energy_enabled'):
        energy_type = data['energy_type']
        daily_count = int(data['energy_daily'])
        
        price = DRINKS_DATA['energy'][energy_type]['price']
        brands = DRINKS_DATA['energy'][energy_type]['brands']
        
        daily_cost = daily_count * price
        weekly_cost = daily_cost * 7
        monthly_cost = daily_cost * 30
        yearly_cost = daily_cost * 365
        
        results['breakdown'].append({
            'type': 'Енергетики',
            'subtype': energy_type,
            'brands': brands,
            'daily': daily_cost,
            'weekly': weekly_cost,
            'monthly': monthly_cost,
            'yearly': yearly_cost
        })
        
        results['total_cost_day'] += daily_cost
        results['total_cost_week'] += weekly_cost
        results['total_cost_month'] += monthly_cost
        results['total_cost_year'] += yearly_cost
        
        if daily_count >= 3:
            results['diseases'].extend(DISEASES['energy'])
    
    # Розрахунок алкоголю
    if data.get('alcohol_enabled'):
        alcohol_type = data['alcohol_type']
        daily_count = int(data['alcohol_daily'])
        
        price = DRINKS_DATA['alcohol'][alcohol_type]['price']
        brands = DRINKS_DATA['alcohol'][alcohol_type]['brands']
        
        daily_cost = daily_count * price
        weekly_cost = daily_cost * 7
        monthly_cost = daily_cost * 30
        yearly_cost = daily_cost * 365
        
        results['breakdown'].append({
            'type': 'Слабоалкогольні напої',
            'subtype': alcohol_type,
            'brands': brands,
            'daily': daily_cost,
            'weekly': weekly_cost,
            'monthly': monthly_cost,
            'yearly': yearly_cost
        })
        
        results['total_cost_day'] += daily_cost
        results['total_cost_week'] += weekly_cost
        results['total_cost_month'] += monthly_cost
        results['total_cost_year'] += yearly_cost
        
        if daily_count >= 3:
            results['diseases'].extend(DISEASES['alcohol'])
    
    # Розрахунок кави
    if data.get('coffee_enabled'):
        coffee_type = data['coffee_type']
        daily_count = int(data['coffee_daily'])
        
        price = DRINKS_DATA['coffee'][coffee_type]['price']
        brands = DRINKS_DATA['coffee'][coffee_type]['brands']
        
        daily_cost = daily_count * price
        weekly_cost = daily_cost * 7
        monthly_cost = daily_cost * 30
        yearly_cost = daily_cost * 365
        
        results['breakdown'].append({
            'type': 'Кава',
            'subtype': coffee_type,
            'brands': brands,
            'daily': daily_cost,
            'weekly': weekly_cost,
            'monthly': monthly_cost,
            'yearly': yearly_cost
        })
        
        results['total_cost_day'] += daily_cost
        results['total_cost_week'] += weekly_cost
        results['total_cost_month'] += monthly_cost
        results['total_cost_year'] += yearly_cost
        
        if daily_count >= 3:
            results['diseases'].extend(DISEASES['coffee'])
    
    # Розрахунок газованих напоїв
    if data.get('soda_enabled'):
        soda_type = data['soda_type']
        daily_count = int(data['soda_daily'])
        
        price = DRINKS_DATA['soda'][soda_type]['price']
        brands = DRINKS_DATA['soda'][soda_type]['brands']
        
        daily_cost = daily_count * price
        weekly_cost = daily_cost * 7
        monthly_cost = daily_cost * 30
        yearly_cost = daily_cost * 365
        
        results['breakdown'].append({
            'type': 'Газовані напої',
            'subtype': soda_type,
            'brands': brands,
            'daily': daily_cost,
            'weekly': weekly_cost,
            'monthly': monthly_cost,
            'yearly': yearly_cost
        })
        
        results['total_cost_day'] += daily_cost
        results['total_cost_week'] += weekly_cost
        results['total_cost_month'] += monthly_cost
        results['total_cost_year'] += yearly_cost
        
        if daily_count >= 2:
            results['diseases'].extend(DISEASES['soda'])
    
    # Розрахунок куріння
    if data.get('smoking_enabled'):
        smoking_type = data['smoking_type']
        
        if smoking_type == 'cigarettes':
            daily_count = int(data['cigarettes_daily'])
            price_per_cigarette = SMOKING_DATA['cigarettes']['price_per_cigarette']
            
            daily_cost = daily_count * price_per_cigarette
            weekly_cost = daily_cost * 7
            monthly_cost = daily_cost * 30
            yearly_cost = daily_cost * 365
            
            results['breakdown'].append({
                'type': 'Цигарки',
                'subtype': 'Традиційні',
                'brands': ['Різні бренди'],
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            if daily_count >= 10:
                results['diseases'].extend(DISEASES['smoking'])
        
        elif smoking_type == 'vape_disposable':
            monthly_count = int(data['vape_disposable_monthly'])
            price_per_vape = SMOKING_DATA['vape']['disposable']['price']
            
            daily_cost = (monthly_count * price_per_vape) / 30
            weekly_cost = (monthly_count * price_per_vape) / 4.33
            monthly_cost = monthly_count * price_per_vape
            yearly_cost = monthly_cost * 12
            
            results['breakdown'].append({
                'type': 'Електронні сигарети',
                'subtype': 'Одноразові',
                'brands': ['Різні бренди'],
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            if monthly_count >= 4:
                results['diseases'].extend(DISEASES['smoking'])
        
        elif smoking_type == 'vape_reusable':
            maintenance_cost = SMOKING_DATA['vape']['reusable']['monthly_maintenance']
            
            daily_cost = maintenance_cost / 30
            weekly_cost = maintenance_cost / 4.33
            monthly_cost = maintenance_cost
            yearly_cost = maintenance_cost * 12
            
            results['breakdown'].append({
                'type': 'Електронні сигарети',
                'subtype': 'Багаторазові',
                'brands': ['Різні бренди'],
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            results['diseases'].extend(DISEASES['smoking'])
        
        elif smoking_type == 'hookah':
            weekly_sessions = int(data['hookah_weekly'])
            session_price = SMOKING_DATA['hookah']['price_per_session']
            
            daily_cost = (weekly_sessions * session_price) / 7
            weekly_cost = weekly_sessions * session_price
            monthly_cost = weekly_cost * 4.33
            yearly_cost = weekly_cost * 52
            
            results['breakdown'].append({
                'type': 'Кальян',
                'subtype': 'У закладах',
                'brands': ['Кальянні'],
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            if weekly_sessions >= 3:
                results['diseases'].extend(DISEASES['smoking'])
    
    # Розрахунок фастфуду
    if data.get('junk_food_enabled'):
        food_type = data['junk_food_type']
        
        if food_type == 'chips':
            weekly_packs = int(data['chips_weekly'])
            price_per_pack = JUNK_FOOD_DATA['chips']['price_per_pack']
            brands = JUNK_FOOD_DATA['chips']['brands']
            
            daily_cost = (weekly_packs * price_per_pack) / 7
            weekly_cost = weekly_packs * price_per_pack
            monthly_cost = weekly_cost * 4.33
            yearly_cost = weekly_cost * 52
            
            results['breakdown'].append({
                'type': 'Чіпси та снеки',
                'subtype': 'Пакетовані',
                'brands': brands,
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            if weekly_packs >= 3:
                results['diseases'].extend(DISEASES['junk_food'])
        
        elif food_type in ['pizza', 'burgers']:
            weekly_count = int(data[f'{food_type}_weekly'])
            price = JUNK_FOOD_DATA[food_type][data[f'{food_type}_type']]['price']
            brands = JUNK_FOOD_DATA[food_type][data[f'{food_type}_type']]['brands']
            
            daily_cost = (weekly_count * price) / 7
            weekly_cost = weekly_count * price
            monthly_cost = weekly_cost * 4.33
            yearly_cost = weekly_cost * 52
            
            results['breakdown'].append({
                'type': 'Піца' if food_type == 'pizza' else 'Бургери',
                'subtype': data[f'{food_type}_type'],
                'brands': brands,
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            if weekly_count >= 2:
                results['diseases'].extend(DISEASES['junk_food'])
        
        elif food_type == 'sweets':
            weekly_packs = int(data['sweets_weekly'])
            price_per_pack = JUNK_FOOD_DATA['sweets']['price_per_pack']
            brands = JUNK_FOOD_DATA['sweets']['brands']
            
            daily_cost = (weekly_packs * price_per_pack) / 7
            weekly_cost = weekly_packs * price_per_pack
            monthly_cost = weekly_cost * 4.33
            yearly_cost = weekly_cost * 52
            
            results['breakdown'].append({
                'type': 'Солодощі',
                'subtype': 'Шоколадки та цукерки',
                'brands': brands,
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            if weekly_packs >= 4:
                results['diseases'].extend(DISEASES['junk_food'])
    
    # Розрахунок азартних ігор
    if data.get('gambling_enabled'):
        gambling_type = data['gambling_type']
        
        if gambling_type == 'lottery':
            weekly_tickets = int(data['lottery_weekly'])
            price_per_ticket = GAMBLING_DATA['lottery']['price_per_ticket']
            
            daily_cost = (weekly_tickets * price_per_ticket) / 7
            weekly_cost = weekly_tickets * price_per_ticket
            monthly_cost = weekly_cost * 4.33
            yearly_cost = weekly_cost * 52
            
            results['breakdown'].append({
                'type': 'Лотерея',
                'subtype': 'Квитки',
                'brands': ['Національні лотереї'],
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            if weekly_tickets >= 3:
                results['diseases'].extend(DISEASES['gambling'])
        
        elif gambling_type == 'casino':
            casino_type = data['casino_type']
            daily_loss = GAMBLING_DATA['casino'][casino_type]['daily_loss']
            
            daily_cost = daily_loss
            weekly_cost = daily_cost * 7
            monthly_cost = daily_cost * 30
            yearly_cost = daily_cost * 365
            
            results['breakdown'].append({
                'type': 'Казино',
                'subtype': casino_type,
                'brands': ['Онлайн та офлайн казино'],
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            results['diseases'].extend(DISEASES['gambling'])
        
        elif gambling_type == 'betting':
            betting_type = data['betting_type']
            weekly_bet = GAMBLING_DATA['betting'][betting_type]['weekly_bet']
            
            daily_cost = weekly_bet / 7
            weekly_cost = weekly_bet
            monthly_cost = weekly_cost * 4.33
            yearly_cost = weekly_cost * 52
            
            results['breakdown'].append({
                'type': 'Букмекерські ставки',
                'subtype': betting_type,
                'brands': ['Спортивні ставки'],
                'daily': daily_cost,
                'weekly': weekly_cost,
                'monthly': monthly_cost,
                'yearly': yearly_cost
            })
            
            results['total_cost_day'] += daily_cost
            results['total_cost_week'] += weekly_cost
            results['total_cost_month'] += monthly_cost
            results['total_cost_year'] += yearly_cost
            
            results['diseases'].extend(DISEASES['gambling'])
    
    # Вибір ідей для заощаджень на основі річної суми
    if results['total_cost_year'] > 0:
        # Вибираємо 5-8 ідей відповідно до суми
        if results['total_cost_year'] < 30000:
            results['saving_ideas'] = [idea['name'] + ' (' + idea['price'] + ')' for idea in SAVING_IDEAS[:6]]
        elif results['total_cost_year'] < 70000:
            results['saving_ideas'] = [idea['name'] + ' (' + idea['price'] + ')' for idea in SAVING_IDEAS[:10]]
        elif results['total_cost_year'] < 150000:
            results['saving_ideas'] = [idea['name'] + ' (' + idea['price'] + ')' for idea in SAVING_IDEAS[:14]]
        else:
            results['saving_ideas'] = [idea['name'] + ' (' + idea['price'] + ')' for idea in SAVING_IDEAS]
    
    # Видалення дублікатів захворювань
    results['diseases'] = list(set(results['diseases']))
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
