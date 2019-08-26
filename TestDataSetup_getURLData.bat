set SOURCE=%~dp0

SET today=%Date:~10,4%%Date:~4,2%%Date:~7,2%
set t=%time:~0,8%
set t=%t::=%
set t=%t: =0%


echo "drive change"
cd C:
echo "drive path"
C:
cd C:\Mentoring_Minds\mysatori-qa\Wizard_Interface\

echo ********** Executing MM Sample Scripts on Chrome *****************


REM Execute test scripts in AWS system in Chrome browser
call pybot --variable BROWSER:gc --outputdir C:\MM_Results\Chrome_%today%_%t% --test "Add school details to teacher description" C:\Mentoring_Minds\mysatori-qa\Wizard_Interface\Automation_Testsuites\TestSuites\TestDataCreation\TestDataCreation.txt
call pybot --variable BROWSER:gc --outputdir C:\MM_Results\Chrome_%today%_%t% --test "TestDataSetupForSchools_Inprogress" C:\Mentoring_Minds\mysatori-qa\Wizard_Interface\Automation_Testsuites\TestSuites\TestDataCreation\TestDataCreation.txt

python C:\Mentoring_Minds\mysatori-qa\Wizard_Interface\Automation_Testsuites\SendEmail.py  Chrome_%today%_%t%

