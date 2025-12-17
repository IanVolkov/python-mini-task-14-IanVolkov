echo "With GIL:"
for item in 1 2 5 20 50
do 
  PYTHON_GIL=1 python3.14t main.py $item
  echo ''
done

echo "Without GIL:"
for item in 1 2 5 20 50
do
  PYTHON_GIL=0 python3.14t main.py $item
  echo ''
done
