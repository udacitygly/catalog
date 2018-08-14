from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Category, Base, CategoryItem, User

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Optional Load script based off the menu items example in Udacity class

User1 = User(name='Mark', email='glyshaw@gmail.com',
             picture='https://media.licdn.com/dms/image/C4D03AQFtEXt99RTnww/profile-displayphoto-shrink_200_200/0?e=1536796800&v=beta&t=a5UcogWJAcA3zMFq0texdTHW7GGZO4ix8w94LBF1-bc'
             )
session.add(User1)
session.commit()


catalog1 = Category(user_id=1, name='Soccer')

session.add(catalog1)
session.commit()

catalogItem2 = CategoryItem(user_id=1, name='Soccer Ball',
                            description='Lorem ipsum dolor sit amet, ei diceret euismod pro', price='$7.50', category=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem1 = CategoryItem(user_id=1, name='Knee Pads',
                            description='Lorem ipsum dolor sit amet, ei diceret euismod pro',
                            price='$2.99', category=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CategoryItem(user_id=1, name='Elbow Pads',
                            description='Lorem ipsum dolor sit amet, ei diceret euismod pro', price='$5.50', category=catalog1)

session.add(catalogItem2)
session.commit()

catalog2 = Category(user_id=1, name='Basketball')

session.add(catalog2)
session.commit()

catalogItem1 = CategoryItem(user_id=1, name='Teen Regulation Ball',
                            description='Special size for teen players, non-regulation', price='$7.99', category=catalog2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CategoryItem(user_id=1, name='Ball Pump',
                            description='Lorem ipsum dolor sit amet, sit facilisi rationibus ea, justo', price='$25', category=catalog2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CategoryItem(user_id=1, name='Net',
                            description='Lorem ipsum dolor sit amet, sit facilisi rationibus ea, justo', price='15', category=catalog2)

session.add(catalogItem3)
session.commit()

catalog1 = Category(user_id=1, name='Baseball')

session.add(catalog1)
session.commit()

catalogItem1 = CategoryItem(user_id=1, name='Practice Ball',
                            description='Lorem ipsum dolor sit amet, sit facilisi rationibus ea, justo', price='$8.99', category=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CategoryItem(user_id=1, name='Regulation Ball',
                            description='Lorem ipsum dolor sit amet, sit facilisi rationibus ea, justo', price='$6.99', category=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CategoryItem(user_id=1, name='Home Plate',
                            description='Lorem ipsum dolor sit amet, sit facilisi rationibus ea, justo', price='$9.95', category=catalog1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CategoryItem(user_id=1, name='Base Pad',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$6.99', category=catalog1)

session.add(catalogItem4)
session.commit()


catalog1 = Category(user_id=1, name='Frisbee')

session.add(catalog1)
session.commit()

catalogItem1 = CategoryItem(user_id=1, name='Frolf Disc 67 grams',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$2.99', category=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CategoryItem(user_id=1, name='Competition Fisbee',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$5.99', category=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CategoryItem(user_id=1, name='Disc Bag',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$4.50', category=catalog1)

session.add(catalogItem3)
session.commit()


catalog1 = Category(user_id=1, name="Snowboarding")

session.add(catalog1)
session.commit()

catalogItem1 = CategoryItem(user_id=1, name='Snowboard',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$13.95', category=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CategoryItem(user_id=1, name='Snowboard boots',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.',
                            price='$4.95', category=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CategoryItem(user_id=1, name="Regulation Gloves",
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$6.95', category=catalog1)

session.add(catalogItem3)
session.commit()


catalog1 = Category(user_id=1, name="Rock Climbing")

session.add(catalog1)
session.commit()

catalogItem1 = CategoryItem(user_id=1, name='Clips',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$9.95', category=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CategoryItem(user_id=1, name='Spikes',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$7.95', category=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CategoryItem(user_id=1, name='Rope',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$6.50', category=catalog1)

session.add(catalogItem3)
session.commit()


catalog1 = Category(user_id=1, name="Foosball")

session.add(catalog1)
session.commit()

catalogItem9 = CategoryItem(user_id=1, name='Stick Men',
                            description='The little dudes on the pole', price='$8.99', category=catalog1)

session.add(catalogItem9)
session.commit()

catalogItem1 = CategoryItem(user_id=1, name='Ball',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$2.99', category=catalog1)

session.add(catalogItem1)
session.commit()


catalog1 = Category(user_id=1, name='Skating')

session.add(catalog1)
session.commit()

catalogItem1 = CategoryItem(user_id=1, name='Skates',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$5.95', category=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CategoryItem(user_id=1, name='Music Tracks',
                            description='Lorem ipsum dolor sit amet, ut eirmod ponderum.', price='$7.99', category=catalog1)

session.add(catalogItem2)
session.commit()

print 'added catalog items!'
