class Reading < ActiveRecord::Base
    def self.getbill(type, sector, location)
        if type == "gas"
            result = self.where('business_class = ? and gas_billed IS NOT NULL and city_code = ?', sector, location)
        elsif type == "electric"
            result = self.where('business_class = ? and electric_billed IS NOT NULL and city_code = ?', sector, location)
        end
        return result
    end
    
    def self.billsum(type, twp, boro)
        if type == "gas"
            result = twp.pluck(:gas_billed).sum + boro.pluck(:gas_billed).sum
        elsif type == "electric"
            result = twp.pluck(:electric_billed).sum + boro.pluck(:electric_billed).sum
        end
        return result
    end
    
    def self.yeardaterange(data, startdate, enddate)
        result = data.where(read_date: DateTime.new(startdate)..(DateTime.new(enddate) - 1.month))
        result = result.pluck(:read_date).map{|readdate| readdate.strftime("%B, %Y").gsub(/,/, '')}
        return result
    end
    
    def self.yeardatarange(data, type, startdate, enddate)
        result = data.where(read_date: DateTime.new(startdate)..(DateTime.new(enddate) - 1.month))
        if type == "gas"
            result = result.pluck(:gas_billed)
        elsif type == "electric"
            result = result.pluck(:electric_billed)
        end
        return result
    end

end
