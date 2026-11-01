def format_currency(amount):
    """Format currency with Indian numbering"""
    return f"₹{amount:,.2f}"

def get_business_insights(prediction, mrp):
    """Generate business insights based on prediction"""
    multiple = prediction / mrp if mrp > 0 else 0
    
    if multiple > 30:
        return " **Exceptional Performance** - This product shows outstanding revenue potential!"
    elif multiple > 20:
        return "**High Performance** - Strong sales expected for this combination"
    elif multiple > 10:
        return "**Good Performance** - Solid revenue generation predicted"
    elif multiple > 5:
        return "**Moderate Performance** - Consider optimization strategies"
    else:
        return "**Review Required** - Low revenue potential, reassess pricing/placement"
