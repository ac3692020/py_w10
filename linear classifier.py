#linear classifier
import numpy as np
import matplotlib.pyplot as  plt
from sklearn.model_selection import train_test_split,KFold

# %%#linear classifier
np.random.seed(0)

# %%
dogs_whisker_length = np.random.normal(loc=5,scale=1, size =10)
dogs_earflapiness_index = np.random.normal(loc= 8, scale=1,size=10)

# %%
cats_whisker_length = np.random.normal(loc=8,scale=1, size =10)
cats_earflapiness_index = np.random.normal(loc=5, scale=1,size=10)

# %%
dogs_data=np.vstack((dogs_whisker_length,dogs_earflapiness_index)).T
cats_data=np.vstack((cats_whisker_length,cats_earflapiness_index)).T
data=np.vstack((dogs_data,cats_data))
labels=np.hstack((np.zeros(len(dogs_data)),np.ones(len(cats_data))))

# %%
X_train,X_test,y_train,y_test=train_test_split(data,labels,test_size=0.2,random_state=42)

# %%
X_test

# %%
X_train

# %%
labels

# %%
plt.scatter(X_train[y_train == 0] [:,0],X_train[y_train == 0] [:,1], label='Training Dogs')
plt.scatter(X_train[y_train == 1] [:,0],X_train[y_train == 1] [:,1] ,label='Training Cats')
plt.scatter(X_test[:, 0], X_test[:, 1], c=y_test, cmap='bwr' ,label='testing data')
plt.xlabel('whisker length')
plt.ylabel('ear flappiness index')  
plt.title('dog vs cat classification -training and testing data')
plt.legend()
plt.show    


# %%
def random_lc(data_dogs, data_cats, k, d):
    best_error = float('inf')  # Initialize with a high value
    best_theta = None
    best_theta0 = None

    for _ in range(k):
        theta = np.random.normal(size=d)
        theta0 = np.random.normal()
        
        error = compute_error(data_dogs, data_cats, theta, theta0)

        if error < best_error:
            best_error = error
            best_theta = theta
            best_theta0 = theta0

    return best_theta, best_theta0, best_error

# %%
def compute_error(data_dogs,data_cats,theta,theta0):
    error=0

    for x_dog in data_dogs :
        if np.dot(theta,x_dog)+theta0 <=0:
            error+= 1

    for x_cat in data_cats :
        if np.dot(theta,x_cat)+theta0 >0:
            error+= 1        
            
    return error / (len(data_dogs) + len(data_cats))      
        


# %%
def cross_validate(data_dogs,data_cats,k_values,d,n_splits=5):
    kf=KFold(n_splits=  n_splits,   shuffle=True,random_state=42)
    avg_errors=[]

    for k in k_values:
        errors=[]

        for train_index, val_index in kf.split(data_dogs):
            X_train_fold=np.vstack((data_dogs[train_index],data_cats[train_index]))
            y_train_fold=np.hstack((np.zeros(len(train_index)),np.ones(len(train_index))))
            X_val_fold=np.vstack((data_dogs[val_index],data_cats[val_index]))
            y_val_fold=np.hstack((np.zeros(len(val_index)),np.ones(len(val_index))))

            

            best_theta_fold, best_theta0_fold, error = random_lc(X_train_fold[y_train_fold==0],X_train_fold[y_train_fold==1],k,d)

            errors.append(compute_error(X_val_fold[y_val_fold==0],X_val_fold[y_val_fold==1],best_theta_fold,best_theta0_fold))

            avg_errors.append(np.mean(errors))

            best_k= k_values[np.argmin(avg_errors)]
    return best_k

            #define best values of k to try
 
k_values=[1,10,50,100,500,750,1000]

best_k= cross_validate(dogs_data,cats_data,k_values,d=2)
print(f"best value of k:{best_k}")           
            

# %%
k=best_k
d=2
best_theta_train,best_theta0_train, train_error = random_lc(X_train[y_train==0],X_train[y_train==1],k,d)

# %%
x_vals_train = np.linspace(2, 10, 1000)
y_vals_train = (-best_theta_train[0] / best_theta_train[1]) * x_vals_train - (best_theta0_train / best_theta_train[1])

# %%
plt.scatter(X_train[y_train == 0] [:,0],X_train[y_train == 0] [:,1], label='Training Dogs')
plt.scatter(X_train[y_train == 1] [:,0],X_train[y_train == 1] [:,1] ,label='Training Cats')
plt.plot(x_vals_train, y_vals_train, color='red', linestyle='--', label='training decesion boundary')
plt.xlim([3.5,11])
plt.ylim([2,10])
plt.xlabel('whisker length')
plt.ylabel('ear flappiness index')  
plt.title('dog vs cat classification -training and testing data')
plt.legend()
plt.show    


# %%
print(f"training error:{train_error} ")

# %%
test_error= compute_error(X_test[y_test==0],X_test[y_test==1],best_theta_train,best_theta0_train)
print(f"testing error:{test_error} ")

# %%
plt.scatter(X_train[y_train == 0] [:,0],X_train[y_train == 0] [:,1], label='Training Dogs')
plt.scatter(X_train[y_train == 1] [:,0],X_train[y_train == 1] [:,1] ,label='Training Cats')

predicted_labels=np.ones_like(y_test)
for i, x_test in enumerate(X_test):
        if np.dot(best_theta_train , x_test) + best_theta0_train > 0:
                predicted_labels[i]= 0

plt.scatter(X_test[predicted_labels==0] [:,0], X_test[predicted_labels==0] [:,1], marker='x', label='predicted dog data')
plt.scatter(X_test[predicted_labels==1] [:,0], X_test[predicted_labels==1] [:,1], marker='x', label='predicted cat data')    

plt.plot(x_vals_train, y_vals_train, color='red', linestyle='--', label='decesion boundary')
plt.xlabel('whisker length')
plt.ylabel('ear flappiness index')  
plt.title('dog vs cat classification: actual vs predicted test data')
plt.legend()
plt.show 

# %%



