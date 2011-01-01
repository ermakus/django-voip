from django.test import TestCase
from django.contrib.auth.models import User

from recommender.models import Recommender, TestItem
from voting.models import Vote
from tagging.models import Tag

class RecommenderManagerTest(TestCase):
    
    def setUp(self):
        
        movies = ['Casablanca','Batman begins','2001','Layer Cake','Diamonds forever','Animal House','Die Hard','Hitch']
        users = ['John', 'Toby', 'Susan', 'Bosco', 'Harry', 'Helen','Mike']
        
        for movie in movies:
            TestItem.objects.create(name=movie)
        for user in users:
            User.objects.create_user(username=user, email=user+'@mockmail.com', password=user)
        
        def _rot(list):
            while True:
                for d in list: yield d
        votes = _rot([1,0,1,-1,-1,1,0,0,1,0,0,1,-1,0,-1,0,-1,1,1,-1,0,0,0,1,0,-1,0,1,1])
        
        users = User.objects.all()
        movies = TestItem.objects.all()
        for user in users:
            for movie in movies:
                Vote.objects.record_vote(movie, user, votes.next())

        movie_tags = ['classic','b&w','romantic','thriller',
                'action','superheros','adventures','fx',
                'science-fiction','fx','classic','thriller',
                'gangsters','action','comedy','thriller',
                'action', 'adventures', 'thriller', 'classic',
                'comedy','teenagers','musical','university',
                'thriller','ny','action','fx',
                'comedy','romantic','modern','ny',
                ]
        user_tags = ['action','adventures','thriller',
                     'romatic','classic','b&w',
                     'romantic','adventures','western',
                     'thriller','gangsters','romantic',
                     'action','fx','gore',
                     'comedy','classic','b&w',
                     'ny','action','fx',]
        i = 0
        for movie in movies:
            while True:
                tag = movie_tags[i]
                Tag.objects.add_tag(movie, tag)
                i+=1   
                if i%4==0: break

        i = 0
        for user in users:
            while True:
                tag = user_tags[i]
                Tag.objects.add_tag(user, tag)
                i+=1   
                if i%3==0: break
                
    def tearDown(self):
        pass
    
    def _print_matrix(self, users, items):
        item_names = [str(item)[0:7] for item in items]
        print '\t' + '\t'.join(item_names)
        for other in users:
            votes_for_user = Vote.objects.get_for_user_in_bulk(items, other)
            votes = []
            for item in items:
                if item.id in votes_for_user:
                    votes.append('%d' % votes_for_user[item.id].vote)
                else:
                    votes.append(' ')
            print str(other)[0:7] +'\t'+ '\t'.join(votes)

    def test_get_best_items_for_user(self):
        users = User.objects.all()
        movies = TestItem.objects.all()
        self._print_matrix(users, movies)
        for user in users:
            recs = Recommender.objects.get_best_items_for_user(user, users, movies)
            print "Best Items found for %s: %s " % (user, recs)

        user = User.objects.get(id=3)
        users = Recommender.objects.get_best_items_for_user(user, users, movies)
        self.assertEqual(len(users),2)
        self.assertEqual(users[0][1].id,7)
        self.assertEqual(users[1][1].id,6)

    def test_get_similar_users(self):
        users = User.objects.all()
        movies = TestItem.objects.all()
        self._print_matrix(users, movies)
        for user in users:
            sim_users = Recommender.objects.get_similar_users(user, users, movies)
            print "Similar users for %s: %s " % (user, sim_users)

        user = User.objects.get(id=6)
        users = Recommender.objects.get_similar_users(user, users, movies)
        self.assertEqual(len(users),3)
        self.assertEqual(users[0][1].id,1)
        self.assertEqual(users[1][1].id,4)
        self.assertEqual(users[2][1].id,3)

    def test_get_best_users_for_item(self):
        users = User.objects.all()
        movies = TestItem.objects.all()
        self._print_matrix(users, movies)
        for movie in movies:
            recs = Recommender.objects.get_best_users_for_item(movie, users, movies)
            print "Best Users found for %s: %s " % (movie, recs)

        movie = TestItem.objects.get(id=5)
        users = Recommender.objects.get_similar_items(movie, users, movies)
        self.assertEqual(len(users),1)
        self.assertEqual(users[0][1].id,4)

    def test_get_similar_items(self):
        users = User.objects.all()
        movies = TestItem.objects.all()
        self._print_matrix(users, movies)
        for movie in movies:
            sim_movies = Recommender.objects.get_similar_items(movie, users, movies)
            print "Similar movies for %s: %s " % (movie, sim_movies)
        
        movie = TestItem.objects.get(id=1)
        sim_movies = Recommender.objects.get_similar_items(movie, users, movies)
        self.assertEqual(len(sim_movies),2)
        self.assertEqual(sim_movies[0][1].id,7)
        self.assertEqual(sim_movies[1][1].id,4)
               
    def test_get_content_based_recs(self):
        users = User.objects.all()
        movies = TestItem.objects.all()

        for user in users:
            sim_movies = Recommender.objects.get_content_based_recs(user, movies)
            print "Best movies based on tags for %s: %s " % (user, sim_movies)

        user = User.objects.get(id=4)
        movies = Recommender.objects.get_content_based_recs(user, movies)
        self.assertEqual(len(movies),2)
        self.assertEqual(movies[0][1].id,1)

    def test_kcluster(self):
        users = User.objects.all()
        movies = TestItem.objects.all()

        user_cluster = Recommender.objects.cluster_users(users, movies)
        print "User Clusters %r" % user_cluster

        item_cluster = Recommender.objects.cluster_items(users, movies)
        print "Item Clusters %r" % item_cluster
