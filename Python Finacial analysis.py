import pandas as pd
import numpy as np
# import yfinance as yf  # Module not found - need to install via pip: pip install yfinance
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# List of Fortune 500 companies (example - you'd want to load the full list)
fortune500_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'BRK-B', 'JPM', 'JNJ', 'V', 'PG', 'UNH']

class FinancialAnalyzer:
    def __init__(self, tickers):
        self.tickers = tickers
        self.companies_data = {}
        
    def fetch_financial_data(self):
        """Fetch 10 years of financial data for each company"""
        for ticker in self.tickers:
            try:
                company = yf.Ticker(ticker)
                
                # Get balance sheet data
                balance_sheet = company.balance_sheet
                
                # Get income statement data
                income_stmt = company.financials
                
                self.companies_data[ticker] = {
                    'balance_sheet': balance_sheet,
                    'income_stmt': income_stmt
                }
                
            except Exception as e:
                print(f"Error fetching data for {ticker}: {str(e)}")
                
    def calculate_key_metrics(self):
        """Calculate important financial metrics"""
        metrics = {}
        
        for ticker, data in self.companies_data.items():
            bs = data['balance_sheet']
            is_ = data['income_stmt']
            
            metrics[ticker] = {
                'ROE': [], # Return on Equity
                'ROA': [], # Return on Assets
                'Profit_Margin': [], # Net Profit Margin
                'Current_Ratio': [], # Current Ratio
                'Debt_to_Equity': [] # Debt to Equity Ratio
            }
            
            for year in bs.columns:
                try:
                    # Calculate metrics for each year
                    net_income = is_.loc['Net Income'][year]
                    total_assets = bs.loc['Total Assets'][year]
                    total_equity = bs.loc['Total Stockholder Equity'][year]
                    current_assets = bs.loc['Total Current Assets'][year]
                    current_liabilities = bs.loc['Total Current Liabilities'][year]
                    total_liabilities = bs.loc['Total Liabilities'][year]
                    revenue = is_.loc['Total Revenue'][year]
                    
                    metrics[ticker]['ROE'].append(net_income / total_equity)
                    metrics[ticker]['ROA'].append(net_income / total_assets)
                    metrics[ticker]['Profit_Margin'].append(net_income / revenue)
                    metrics[ticker]['Current_Ratio'].append(current_assets / current_liabilities)
                    metrics[ticker]['Debt_to_Equity'].append(total_liabilities / total_equity)
                    
                except Exception as e:
                    print(f"Error calculating metrics for {ticker} in {year}: {str(e)}")
                    
        return metrics
    
    def visualize_trends(self, metrics):
        """Create visualizations for financial trends"""
        for metric_name in ['ROE', 'ROA', 'Profit_Margin', 'Current_Ratio', 'Debt_to_Equity']:
            plt.figure(figsize=(12, 6))
            
            for ticker in self.tickers:
                if ticker in metrics:
                    plt.plot(metrics[ticker][metric_name], label=ticker)
            
            plt.title(f'{metric_name} Trend Over 10 Years')
            plt.xlabel('Years')
            plt.ylabel(metric_name)
            plt.legend()
            plt.grid(True)
            plt.show()

# Initialize and run analysis
analyzer = FinancialAnalyzer(fortune500_tickers)
analyzer.fetch_financial_data()
metrics = analyzer.calculate_key_metrics()
analyzer.visualize_trends(metrics)

# Generate summary report
def generate_summary_report(metrics):
    summary = pd.DataFrame()
    
    for ticker in metrics:
        latest_metrics = {
            'ROE': metrics[ticker]['ROE'][-1],
            'ROA': metrics[ticker]['ROA'][-1],
            'Profit_Margin': metrics[ticker]['Profit_Margin'][-1],
            'Current_Ratio': metrics[ticker]['Current_Ratio'][-1],
            'Debt_to_Equity': metrics[ticker]['Debt_to_Equity'][-1]
        }
        summary = pd.concat([summary, pd.DataFrame(latest_metrics, index=[ticker])])
    
    return summary

summary_report = generate_summary_report(metrics)
print("\nSummary Report of Latest Financial Metrics:")
print(summary_report)
