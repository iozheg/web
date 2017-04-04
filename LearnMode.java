package ru.netsevak.smokend;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.Locale;

import android.os.Bundle;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.DialogInterface.OnCancelListener;
import android.content.DialogInterface.OnClickListener;
import android.content.SharedPreferences.Editor;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.support.v7.app.ActionBarActivity;
//import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;

public class LearnMode extends ActionBarActivity {

	// имя настройки
	public static final String APP_PREFERENCES = "SmokEnd";
	public static final String APP_PREFERENCES_MODE = "mode";
	public static final String APP_PREFERENCES_INTERVAL = "interval";
	public static final String APP_PREFERENCES_COEFFICIENT = "coefficient";
	public static final String APP_PREFERENCES_DAY = "day";
	
	SharedPreferences mSettings;
	SmokendDB database;
	SQLiteDatabase sqdb;
	
	AlertDialog.Builder ad;
	AlertDialog.Builder LMfinish;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_learn_mode);
		
		
		
		mSettings = getSharedPreferences(APP_PREFERENCES, Context.MODE_PRIVATE);

		
		ad = new AlertDialog.Builder(this);
		ad.setTitle(R.string.menu_return_title);  // заголовок
        ad.setMessage(R.string.return_dialog_text); // сообщение
        ad.setPositiveButton(R.string.yes_button_text, new OnClickListener() {
            public void onClick(DialogInterface dialog, int arg1) {
            	Editor editor = mSettings.edit();
            	editor.clear();
        		editor.apply();
        		database = new SmokendDB(LearnMode.this);
        		sqdb = database.getWritableDatabase();
        		database.clearTable(sqdb);
        		sqdb.close();
        	    database.close();
            	
            	Intent intent = new Intent(LearnMode.this, MainActivity.class);
				startActivity(intent);
				finish();
            }
        });
        ad.setNegativeButton(R.string.no_button_text, new OnClickListener() {
            public void onClick(DialogInterface dialog, int arg1) {
                
            }
        });
        ad.setCancelable(true);
        ad.setOnCancelListener(new OnCancelListener() {
            public void onCancel(DialogInterface dialog) {
                
            }
        });
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.learn_mode, menu);
		return true;
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) 
		{
	    case R.id.returnmenu:
	        ad.show();
	        return true;
	    case R.id.help:
	    	Intent intent = new Intent(this, HelpActivity.class);
			startActivity(intent);
	        return true;
	    default:
	        return super.onOptionsItemSelected(item);
	    }
	}
	
	@Override
	protected void onStop() {
		super.onStop();
	}
	
	public void SmokedClick(View v){
		database = new SmokendDB(this);
		sqdb = database.getWritableDatabase();
		sqdb.execSQL("INSERT INTO 'SmokedCigaretsLM' ('date', 'time') VALUES (date('now', 'localtime'), time('now', 'localtime'))");
		
		String firstRecordDate = "", firstRecordTime = "";
		int numberOfRecords = 0;
		String lastRecordDate = "", lastRecordTime = "";
		
		Cursor cursor = sqdb.rawQuery("SELECT * FROM 'SmokedCigaretsLM'", null);
	
		cursor.moveToFirst(); //выбираем первую запись из всех
		firstRecordDate = cursor.getString(cursor.getColumnIndex("date"));
		firstRecordTime = cursor.getString(cursor.getColumnIndex("time"));
		cursor.moveToLast(); //выбираем последнюю запись из всех
		lastRecordDate = cursor.getString(cursor.getColumnIndex("date"));
		lastRecordTime = cursor.getString(cursor.getColumnIndex("time"));
		numberOfRecords = cursor.getCount();//количество записей всего
//		Log.i("LOG_TAG", "first date " + firstRecordDate + " and first time " + firstRecordTime);
//		Log.i("LOG_TAG", "first date " + lastRecordDate + " and first time " + lastRecordTime);
//		Log.i("LOG_TAG", "total records " + numberOfRecords);
		
		SimpleDateFormat formate = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss", Locale.getDefault());
		Date firstDate = new Date(), lastDate = new Date();
		try {
			firstDate = formate.parse(firstRecordDate + " " + firstRecordTime);
			lastDate = formate.parse(lastRecordDate + " " + lastRecordTime);
		} catch (ParseException e) {
			e.printStackTrace();
			cursor.close();
		}
		
		double totalTime = (double)(lastDate.getTime()/1000 - firstDate.getTime()/1000)/3600;
//		Log.i("LOG_TAG", "totalTime " + totalTime);
		if(totalTime >= 72){
			//если разница между первой выкуренной в режиме обучения и последней равна или больше 72 часов, то заканчиваем режим обучения, начинаем основной режим
			String[] dates = new String[4];
			int i =0;
			
			cursor = sqdb.rawQuery("SELECT `date` FROM 'SmokedCigaretsLM'", null);
			cursor.moveToFirst();
			dates[0] = cursor.getString(cursor.getColumnIndex("date"));
			while (cursor.moveToNext() && i != 3) { //в массив вносим все даты
				if(!dates[i].equals(cursor.getString(cursor.getColumnIndex("date")))){
					dates[++i] = cursor.getString(cursor.getColumnIndex("date"));
				}
			}
			
			i = 0;
			double[] interval = {0,0,0,0};
			double commonInterval = 0;
			
			//для каждой даты выбираем все записи времени, по ним вычисляем интервал для каждой даты
			while(i < 4 && dates[i] != null){
				cursor = sqdb.rawQuery("SELECT time FROM 'SmokedCigaretsLM' WHERE date LIKE '%" + dates[i] + "%'", null);
				cursor.moveToFirst(); //выбираем первую запись для этой даты
				firstRecordDate = dates[i];
				firstRecordTime = cursor.getString(cursor.getColumnIndex("time"));
				cursor.moveToLast(); //выбираем последнюю запись для этой даты
				lastRecordDate = dates[i];
				lastRecordTime = cursor.getString(cursor.getColumnIndex("time"));
				numberOfRecords = cursor.getCount();//количество записей для этой даты
				try {
					firstDate = formate.parse(firstRecordDate + " " + firstRecordTime);
					lastDate = formate.parse(lastRecordDate + " " + lastRecordTime);
				} catch (ParseException e) {
					e.printStackTrace();
					cursor.close();
				}
				interval[i] = ((double)(lastDate.getTime() - firstDate.getTime())/60000)/numberOfRecords;
				i++;
			}
			int j;
			for(i = 0, j = 0; i < 4; i++){	//считаем средний интервал по дням
					if(interval[i] != 0){
						commonInterval += interval[i];
						j++;
					}
			}
			commonInterval = commonInterval/j;
			
			double coefficient = 1.1;
			
			//определяем коэффициент
			if(commonInterval >= 96)
				coefficient = 1.06;
			else if(commonInterval >= 70 && commonInterval < 96)
				coefficient = 1.07;
			else if(commonInterval >= 60 && commonInterval < 70)
				coefficient = 1.08;
			else if(commonInterval >= 60 && commonInterval < 50)
				coefficient = 1.09;
			
//			Log.i("LOG_TAG", "inteval " +commonInterval);
			cursor.close();
			//remember interval in preferences
			Editor editor = mSettings.edit();
			editor.putInt(APP_PREFERENCES_INTERVAL, (int)(commonInterval*60));
			editor.putFloat(APP_PREFERENCES_COEFFICIENT, (float) coefficient);
			editor.putInt(APP_PREFERENCES_DAY, Calendar.getInstance().get(Calendar.DATE));
			editor.putString(APP_PREFERENCES_MODE, "main");
			editor.apply();
			
			LMfinish = new AlertDialog.Builder(this);
			LMfinish.setTitle(R.string.learn_mode_finish_dialog_title);  // заголовок
			LMfinish.setMessage(R.string.learn_mode_finish_dialog_text); // сообщение
			LMfinish.setNegativeButton("OK", new OnClickListener() {
	            public void onClick(DialogInterface dialog, int arg1) {
	            //	database.clearTable(sqdb);
	            	sqdb.close();
	        		database.close();
	        		
	            	Intent intent = new Intent(LearnMode.this, MainModeActivity.class);
					startActivity(intent);
					finish();
	            }
	        });
			LMfinish.setCancelable(false);
			LMfinish.setOnCancelListener(new OnCancelListener() {
	            public void onCancel(DialogInterface dialog) {
	                
	            }
	        });
			LMfinish.show();
		}
		cursor.close();
		sqdb.close();
		database.close();
	}

}
