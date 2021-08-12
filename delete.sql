-- remove some dirty data
DELETE FROM DATA WHERE URL LIKE "htt%://%/oauth/%";
DELETE FROM DATA WHERE URL LIKE "htt%://%/user/login%";
DELETE FROM DATA WHERE URL LIKE "htt%://%/login%";
DELETE FROM DATA WHERE URL LIKE "htt%://%/user/register%";
DELETE FROM DATA WHERE URL LIKE "htt%://%/user/signin%";
DELETE FROM DATA WHERE URL LIKE "htt%://%/user-signin%";
DELETE FROM DATA WHERE URL LIKE "htt%://%/register%";
DELETE FROM DATA WHERE URL LIKE "htt%://%/user-register%";
DELETE FROM DATA WHERE URL LIKE "htt%://%/wp-login.php%";
DELETE FROM DATA WHERE URL LIKE "https://passport.baidu.com/%?login%";
DELETE FROM DATA WHERE URL LIKE "https://signup.microsoft.com/Start%";